from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as lazy
from validate_email import validate_email
import time
import boto3
from boto3.s3.transfer import S3Transfer
from django.conf import settings

# can verify smtp if needed , pip install pyDNS,
# https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address


def validate_email(email):
    is_valid = validate_email('example@example.com')
    if not is_valid:
        raise ValidationError(
            lazy('%(email)s is not valid email'),
            params={'email': email},
        )


def upload_to_s3(file, company_name):
    file_arr = file.name.split(".")
    s = file_arr[0]
    s = s.strip()
    s = s.replace(" ", "")
    file_arr[0] = s
    file_name = file_arr[0] + "_" + str(int(time.time())) + "." + file_arr[1]
    # file_extension = file_arr[1]

    # Saving file into my local machine(or server)
    FILENAME = "/tmp/%s" % (file_name or "")
    with open(FILENAME, "wb") as f:
        f.write(file.read())

    region = settings.AWS_REGION
    bucket = settings.BUCKET_NAME
    key = 'Company/%s/%s' % (company_name, file_name)
    credentials = {'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
                   'aws_secret_access_key': settings.AWS_SECRET_KEY}
    client = boto3.client('s3', region, **credentials)

    transfer = S3Transfer(client)
    transfer.upload_file(FILENAME, bucket, key, extra_args={'ACL': 'public-read'})
    file_url = '%s/%s/%s' % (client.meta.endpoint_url, bucket, key)
    return file_url