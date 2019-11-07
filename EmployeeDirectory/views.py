from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from hr_dashboard.response import api_response
from .models import *
import os, sys
import openpyxl
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
        # print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        return {"success": 1, "data": "", 'message': 'Successfully received',
                'statusCode': 200}