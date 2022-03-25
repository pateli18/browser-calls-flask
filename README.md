## Quickstart

### Create a TwiML App

This project is configured to use a **TwiML App**, which allows us to easily set
the voice URLs for all Twilio phone numbers we purchase in this app.

Create a new TwiML app [here](https://www.twilio.com/user/account/apps/add) and
use its `SID` as the `TWIML_APPLICATION_SID` environment variable wherever you
run this app.


![Creating a TwiML App](http://howtodocs.s3.amazonaws.com/call-tracking-twiml-app.gif)

Once you have created your TwiML app, configure your Twilio phone number to use
it ([instructions here](https://www.twilio.com/help/faq/twilio-client/how-do-i-create-a-twiml-app)).
If you don't have a Twilio phone number yet, you can purchase a new number in
your [Twilio Account Dashboard](https://www.twilio.com/user/account/phone-numbers/incoming).

## Local development

1. To run the app locally, first clone this repository and `cd` into it.

1. Create and activate a new python3 virtual environment.

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

1. Install the requirements using pip.

    ```bash
    pip install -r requirements.txt
    ```

1. Copy the `.env.example` file to `.env`, and edit it including your credentials
   for the Twilio API (found at https://www.twilio.com/user/account/settings). You
   will also need a [Twilio Number](https://www.twilio.com/user/account/phone-numbers/incoming) and TwiML App SID you made above. You will also need a [SECRET_KEY](https://flask.palletsprojects.com/en/2.0.x/config/#SECRET_KEY). 

1. Start ngrok.

   To actually forward incoming calls, your development server will need to be publicly accessible.
   [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).
   
   ```bash
   ngrok http 5002
   ```

   Once you have started ngrok, update your TwiML app's voice URL setting to use your ngrok hostname. It will look something like this:

   ```
   http://[your-domain].ngrok.io/support/call
   ```

1. Start the development server from the root of the directory.

    ```bash
    uvicorn voice_task.server:app --reload --port 5002
    ```

Once ngrok is running, open up your browser and go to your ngrok URL.

That's it!