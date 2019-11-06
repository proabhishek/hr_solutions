import re
import boto3
from decouple import config
from django.conf import settings


def normalise_phone(phone):
    a = re.findall('\d+', phone)
    seperator = ''
    new_phone = seperator.join(a)
    return new_phone[-10:]


# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id=config("ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_KEY"),
    region_name=config("AWS_REGION")
)


# Send your sms message.
def notify(phone, message):
    import pdb
    pdb.set_trace()
    client.publish(
    PhoneNumber=phone,
    Message=message
    )