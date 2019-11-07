from django.urls import path
from .views import *

urlpatterns = [
    path('bulk-update/', BulkEmployeeUpdateExcel.as_view(),  name='bulk-update')
    ]