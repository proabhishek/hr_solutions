from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.utils import timezone
from helpers import upload_to_s3
from hr_dashboard.response import api_response
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import uuid
import time
import boto3
from boto3.s3.transfer import S3Transfer
from django.conf import settings
import datetime
import random
from common import common


def generate_auth_token():
    return uuid.uuid4()


def remove_all_sapce(s):
    s = s.strip()
    s = s.replace(" ", "")
    return s


def generate_otp():
    random_no = str(int(random.randint(1001, 9999)))
    return int(str(random_no)[0:4])


def prepare_message(otp):
    return "Otp for Hr Application is %s" %(otp)


def send_message(phone, organization):
    # phone = common.normalise_phone(phone)
    otp = generate_otp()
    message = prepare_message(otp)
    code = "+91"
    phone = code + phone
    organization.otp = otp
    organization.otp_sent_at = timezone.now()
    organization.save()
    common.notify(phone, message)


class OrganizationSignUpView(APIView):
    permission_classes = (AllowAny,)
    @api_response
    def post(self, request):
        organization_email = request.data['email']
        password = request.data['password']
        company_name = request.data['company_name']
        company_keyword = request.data['company_keyword']
        if not organization_email or not password:
            return {"success": 0, "data": "", 'message': 'Fields cannot be blank', 'statusCode': 400}
        if not company_name:
            return {"success": 0, "data": "", 'message': 'Company Name is missing', 'statusCode': 400}
        if not company_keyword:
            return {"success": 0, "data": "", 'message': 'Company Keyword is missing', 'statusCode': 400}
        organization_duplicate_email = OrganizationSetUp.objects.filter(organization_email=request.data['email'])
        if organization_duplicate_email:
            return {"success": 0, "data": "", 'message': 'Organization already exists with this email',
                    'statusCode': 400}
        organization = OrganizationSetUp.objects.create(organization_email=organization_email,
                                                        password=password, company_name=company_name, company_keyword=company_keyword)
        if organization:
            auth_token = generate_auth_token()
            while OrganizationSetUp.objects.filter(auth_token=auth_token):
                auth_token = generate_auth_token()
            organization.auth_token = auth_token
            organization.save()
            return {"success": 1, "data": {"name": organization.company_name, "email": organization.organization_email,
                                           "company_keyword": organization.company_keyword, "auth-token": organization.auth_token},
                    'message': 'Successfully Signed Up', 'statusCode': 200}


class CompanyKeywordView(APIView):
    permission_classes = (AllowAny,)
    @api_response
    def post(self, request):
        company_keyword = request.data['company_keyword']
        if not company_keyword:
            return {"success": 0, "data": "", 'message': 'Company Keyword is missing', 'statusCode': 400}
        duplicate_company_keyword = OrganizationSetUp.objects.filter(company_keyword=company_keyword)
        if duplicate_company_keyword:
            return {"success": 0, "data": "", 'message': 'Already Exists, Please chose a new one',
                    'statusCode': 400}
        return {"success": 1, "data": "", 'message': '',
                'statusCode': 200}


class OrganizationSetUP(APIView):
    permission_classes = (AllowAny,)
    @api_response
    def post(self, request):
        auth_token = request.META.get('HTTP_AUTH_TOKEN', '')
        organization = OrganizationSetUp.objects.filter(auth_token=auth_token)
        if not organization:
            return {'success': 0, 'error': "Token Missing", 'data': {}, 'statusCode': 400}
        organization = organization[0]
        organization.logo_url = request.data['logo_url']
        organization.tagline = request.data['tagline']
        organization.pan_link = request.data['pan_link']
        organization.contact_number = request.data['contact_number']
        organization.office_address = request.data['office_address']
        organization.save()
        return {"success": 1, "data":"", 'message': 'Updated successfully',
                    'statusCode': 200}


class SignInView(APIView):
    permission_classes = (AllowAny,)
    @api_response
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        organization = OrganizationSetUp.objects.filter(organization_email=email)
        if not organization:
            return {"success": 0, "data": "", 'message': 'Email id doesnot exists', 'statusCode': 400}
        if organization[0].password == password:
            auth_token = generate_auth_token()
            while OrganizationSetUp.objects.filter(auth_token=auth_token):
                auth_token = generate_auth_token()
            organization[0].auth_token = auth_token
            organization[0].save()
            return {"success": 1, "data": {"auth_token": auth_token}, 'message': 'Sign In Successfully', 'statusCode': 200}


class UploadView(APIView):
    permission_classes = (AllowAny,)
    @api_response
    def post(self, request):
        auth_token = request.META.get('HTTP_AUTH_TOKEN', '')
        if not auth_token:
            return {'success': 0, 'error': "Token Missing", 'data': {}, 'statusCode': 400}
        organization = OrganizationSetUp.objects.filter(auth_token=auth_token)
        if not organization:
            return {'success': 0, 'error': "Organization not found", 'data': {}, 'statusCode': 400}
        file = request.data.get('file')
        if file.size > (1024 * 1024 * 5):  # File more than 5 MB shouldn't be allowed
            return {'success': 0, 'error': "File more than 5 MB is not allowed!", 'data': {}, 'statusCode': 400}
        file_arr = file.name.split(".")
        file_arr[0] = remove_all_sapce(file_arr[0])
        file_name = file_arr[0] + "_" + str(int(time.time())) + "." + file_arr[1]
        company_name = remove_all_sapce(organization[0].company_name)
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
        if file_url:
            return {"success": 1, "data": file_url, 'message': 'Uploaded successfully',
                    'statusCode': 200}


class OtpSendView(APIView):
    permission_classes = (AllowAny,)
    @api_response
    def post(self, request):
        auth_token = request.META.get('HTTP_AUTH_TOKEN', '')
        if not auth_token:
            return {'success': 0, 'error': "Token Missing", 'data': {}, 'statusCode': 400}
        organization = OrganizationSetUp.objects.filter(auth_token=auth_token)
        phone = request.data.get('phone')
        send_message(phone, organization[0])
        return {'success': True, 'message': "Otp sent successfully"}


class VerifyOtp(APIView):
    permission_classes = (AllowAny,)

    @api_response
    def post(self, request):
        auth_token = request.META.get('HTTP_AUTH_TOKEN', '')
        if not auth_token:
            return {'success': 0, 'error': "Token Missing", 'data': {}, 'statusCode': 400}
        organization = OrganizationSetUp.objects.filter(auth_token=auth_token)
        if not organization:
            return {"success": 0, "data": "", 'message': 'Organization doesnot exists', 'statusCode': 400}
        otp = request.data.get('otp')
        if int(organization[0].otp) == int(otp):
            return {'success': 1, 'message': "Correct Otp", 'data': ""}
        else:
            return {'success': 0, 'message': "Wrong Otp"}


class Logout(APIView):
    permission_classes = (AllowAny,)

    @api_response
    def delete(self, request):
        auth_token = request.META.get('HTTP_AUTH_TOKEN', '')
        if not auth_token:
            return {'success': 0, 'error': "Token Missing", 'data': {}, 'statusCode': 400}
        organization = OrganizationSetUp.objects.filter(auth_token=auth_token)
        if not organization:
            return {"success": 0, "data": "", 'message': 'Organization doesnot  exists', 'statusCode': 400}
        organization[0].auth_token = ""
        organization[0].save()
        return {"success": 1, "data": "", 'message': 'Logged Out Successfully',
                'statusCode': 200}