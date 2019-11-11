from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import *
from .serializers import *
import string
import random

from hr_dashboard.response import api_response
from .models import *
import os, sys
import openpyxl
from common import common
# Create your views here.


class BulkEmployeeUpdateExcel(APIView):
    permission_classes = (AllowAny,)

    @api_response
    def post(self, request):
        # import pdb
        # pdb.set_trace()
        excel_file = request.data.get('excel-file')
        wb = openpyxl.load_workbook(excel_file)
        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        # length = len(excel_data)
        # i = 1
        # while i<length:
        #     try:
        #         data = excel_data[i]
        #         password = ''.join(random.choices(string.ascii_lowercase +
        #                                           string.digits, k = 8))

            #     employee = Employee.objects.create(
            #         name=data[0],
            #         employee_id = data[1],
            #         designation = data[2],
            #         department = data[3],
            #         pan_card_number = data[4],
            #         email = data[5],
            #         phone = data[6],
            #         date_of_birth = data[7],
            #         date_of_joining = data[8],
            #         blood_group = data[9],
            #         emergency_contact = data[10],
            #         confirmation_date = data[11],
            #         date_of_exit = data[12],
            #         password = password
            #     )
            #     # if employee:
            #     #     auth_token = common.generate_auth_token()
            #     #     while Employee.objects.filter(auth_token=auth_token):
            #     #         auth_token = common.generate_auth_token()
            #     #     employee.auth_token = auth_token
            #     #     employee.save()
            #     i = i + 1
            # except Exception as e:
            #     return {"success": 0, "data": "", 'message': e.message,
            #             'statusCode': 400}
            #     # return {"success": 0, "data": "", 'message': "exception",
            #     #         'statusCode': 400}

        return {"success": 1, "data": excel_data, 'message': 'Successfully received',
                'statusCode': 200}


# class EmployeeUpdate(APIView):
#     permission_classes = (AllowAny,)
#
#     @api_response
#     def post(self, request):
#         name = request.data['name']
#         employee_number = request.data['employee_number']
#         designation = request.data['designation']
#         department = request.data['department']
#         pic_url = request.data['pic_url']
#         pan_card_number = request.data['pan_card_number']
#         email = request.data['email']
#         phone = request.data['phone']
#         date_of_birth = request.data['date_of_birth']
#         date_of_joining = request.data['date_of_joining']
#         password = request.data['password']


class SignInView(APIView):
    permission_classes = (AllowAny,)
    @api_response
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        employee = Employee.objects.filter(email=email)
        if not employee:
            return {"success": 0, "data": "", 'message': 'Email id doesnot exists', 'statusCode': 400}
        if employee[0].password == password:
            auth_token = common.generate_auth_token()
            while Employee.objects.filter(auth_token=auth_token):
                auth_token = common.generate_auth_token()
            employee[0].auth_token = auth_token
            employee[0].save()
            return {"success": 1, "data": {"auth_token": auth_token}, 'message': 'Sign In Successfully', 'statusCode': 200}


class ResetPassword(APIView):
    permission_classes = (AllowAny,)
    @api_response
    def post(self, request):
        auth_token = request.META.get('HTTP_AUTH_TOKEN', '')
        if not auth_token:
            return {'success': 0, 'error': "Token Missing", 'data': {}, 'statusCode': 400}
        employee = Employee.objects.filter(auth_token=auth_token)
        if not employee:
            return {'success': 0, 'error': "Employee not found", 'data': {}, 'statusCode': 400}
        password = request.data['password']
        employee[0].password = password
        employee[0].save()
        return {"success": 1, "data": "", 'message': 'Password Changed successfully', 'statusCode': 200}


class ChangePassword(APIView):
    permission_classes = (AllowAny,)
    @api_response
    def post(self, request):
        auth_token = request.META.get('HTTP_AUTH_TOKEN', '')
        if not auth_token:
            return {'success': 0, 'error': "Token Missing", 'data': {}, 'statusCode': 400}
        employee = Employee.objects.filter(auth_token=auth_token)
        if not employee:
            return {'success': 0, 'error': "Employee not found", 'data': {}, 'statusCode': 400}
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        if not  employee[0].password == old_password:
            return {'success': 0, 'error': "Old Password dinot match", 'data': {}, 'statusCode': 400}
        employee[0].password = new_password
        employee[0].save()
        return {"success": 1, "data": "", 'message': 'Password CHanged successfully', 'statusCode': 200}


class Logout(APIView):
    permission_classes = (AllowAny,)

    @api_response
    def delete(self, request):
        auth_token = request.META.get('HTTP_AUTH_TOKEN', '')
        if not auth_token:
            return {'success': 0, 'error': "Token Missing", 'data': {}, 'statusCode': 400}
        employee = Employee.objects.filter(auth_token=auth_token)
        if not employee:
            return {"success": 0, "data": "", 'message': 'Organization doesnot  exists', 'statusCode': 400}
        employee[0].auth_token = ""
        employee[0].save()
        return {"success": 1, "data": "", 'message': 'Logged Out Successfully',
                'statusCode': 200}