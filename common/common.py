import re
import boto3
from decouple import config
from django.conf import settings
import uuid


def normalise_phone(phone):
    a = re.findall('\d+', phone)
    seperator = ''
    new_phone = seperator.join(a)
    return new_phone[-10:]


# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id="AKIA3OEA3OHXLISUDK2N",
    aws_secret_access_key="7bBgRtoPQuNT99egVg7zBOaT2jNT3Ue+RnnxTrZy",
    region_name="us-east-1"
)


# Send your sms message.
def notify(phone, message):
    client.publish(
        PhoneNumber=phone,
        Message=message
    )


def generate_auth_token():
    return uuid.uuid4()