from enum import Enum
from functools import lru_cache
import json
import requests
import boto3
import os
from typing import List, Optional
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant

from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.rest import Client
from fastapi import FastAPI, Request, status, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

BUCKET = os.environ["BUCKET"]

class Status(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class TwilioToken(BaseModel):
    token: str

class Alternative(BaseModel):
    confidence: str
    content: str

class TranscriptItem(BaseModel):
    start_time: Optional[str]
    end_time: Optional[str]
    alternatives: List[Alternative]
    type: str

class Transcript(BaseModel):
    transcript: str

class TranscriptionResult(BaseModel):
    transcripts: List[Transcript]
    items: List[TranscriptItem]

class TranscriptionResponse(BaseModel):
    status: Status
    results: Optional[TranscriptionResult]


app = FastAPI()
app.mount("/static", StaticFiles(directory="voice_task/static"), name="static")
templates = Jinja2Templates(directory="voice_task/templates")

@app.get('/')
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/support/token', response_model=TwilioToken)
def get_token() -> TwilioToken:
    # Create access token with credentials
    access_token = AccessToken(
        os.environ['TWILIO_ACCOUNT_SID'],
        os.environ['TWILIO_API_KEY'],
        os.environ['TWILIO_API_SECRET'],
        identity="customer"
    )

    # Create a Voice grant and add to token
    voice_grant = VoiceGrant(
        outgoing_application_sid=os.environ['TWIML_APPLICATION_SID'],
        incoming_allow=True,  # Optional: add to allow incoming calls
    )
    access_token.add_grant(voice_grant)

    token = access_token.to_jwt().decode()
    print(token)

    return TwilioToken(token=token)

@app.get('/support/call')
def call(phone_number: str) -> str:
    """Returns TwiML instructions to Twilio's POST requests"""
    print(phone_number)
    response = VoiceResponse()

    dial = Dial(callerId=os.environ['TWILIO_NUMBER'], record="record-from-answer-dual")
    dial.number(phone_number)

    return Response(content=str(response.append(dial)), media_type="text/html") 

@lru_cache(maxsize=20)
def _retrieve_and_save_audio(recording_uri: str, recording_prefix: str):
    response = requests.get(f"https://api.twilio.com{recording_uri}", auth=(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"]))
    audio_contents = response.content

    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=BUCKET, Key=recording_prefix, Body=audio_contents, ContentType="audio/mpeg")

    return f"s3://{BUCKET}/{recording_prefix}"

@lru_cache(maxsize=20)
def _load_transcript(prefix: str) -> dict:
    print(prefix)
    s3_client = boto3.client("s3")
    json_bytes = s3_client.get_object(Bucket=BUCKET, Key=prefix)["Body"].read() 
    return json.loads(json_bytes)


def _transcribe_audio(media_s3_path: str, recording_sid: str, output_prefix: str) -> TranscriptionResponse:
    client = boto3.client("transcribe")
    args = {
        "TranscriptionJobName": recording_sid,
    }
    try:
        response = client.start_transcription_job(
            **args,
            LanguageCode="en-AB",
            MediaFormat="mp3",
            Media={
                "MediaFileUri": media_s3_path,
            },
            OutputBucketName=BUCKET,
            OutputKey=output_prefix,
        )
    # if job already created get result
    except client.exceptions.ConflictException:
        response = client.get_transcription_job(
            **args,
        )

    status = response["TranscriptionJob"]["TranscriptionJobStatus"]
    if status == Status.IN_PROGRESS:
        transcription = None
    # if complete download results
    elif status == Status.COMPLETED:
        transcription = _load_transcript(output_prefix)["results"]
    else:
        raise ValueError(f"unknown status {status}")

    return TranscriptionResponse(status=status, results=transcription)


@app.get('/transcribe/{call_sid}', response_model=TranscriptionResponse)
def transcribe(call_sid: str) -> TranscriptionResponse:
    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
    recordings = client.recordings.list(call_sid=call_sid, limit=20)
    if len(recordings) == 0:
        return TranscriptionResponse(status=Status.IN_PROGRESS, results=None)
    recording = recordings[0]
    if recording.status != "completed":
        return TranscriptionResponse(status=Status.IN_PROGRESS, results=None)

    recording_prefix = f"dev/phone-calls/{recording.sid}.mp3"
    recording_uri = recording.uri.replace('json', 'mp3')

    media_s3_path = _retrieve_and_save_audio(recording_uri, recording_prefix)
    transcription_response = _transcribe_audio(media_s3_path, recording.sid, recording_prefix.replace("mp3", "json"))

    return transcription_response