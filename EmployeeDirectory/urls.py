from django.urls import path
from .views import *

urlpatterns = [
    path('bulk-update/', BulkEmployeeUpdateExcel.as_view(),  name='bulk-update'),
    path('add-employee/', BulkEmployeeUpdateExcel.as_view(),  name='bulk-update'),
    path('sign-in/', SignInView.as_view(),  name='employee-signin'),
    path('reset-password/', ResetPassword.as_view(),  name='employee-reset-password'),
    path('change-password/', ChangePassword.as_view(),  name='employee-change-password'),
    # path('forgot-password/', SignInView.as_view(),  name='employee-signin'),
    path('logout/', Logout.as_view(),  name='logout'),
    ]