from phonenumbers import is_possible_number
from phonenumbers import parse
from phonenumbers.phonenumberutil import NumberParseException


def is_valid_number(number):
    try:
        return is_possible_number(parse(number))
    except NumberParseException:
        return False
