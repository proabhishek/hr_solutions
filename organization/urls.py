from django.urls import path
from .views import *

urlpatterns = [
    path('sign-up/', OrganizationSignUpView.as_view(),  name='organization-signup'),
    path('sign-in/', SignInView.as_view(),  name='organization-signin'),
    path('upload/', UploadView.as_view(),  name='upload'),
    path('profile/', OrganizationSetUP.as_view(),  name='organization-signup'),
    path('send-otp/', OtpSendView.as_view(),  name='organization-sendotp'),
    path('verify-otp/', VerifyOtp.as_view(),  name='organization-verifyotp'),
    path('keyword/', CompanyKeywordView.as_view(),  name='organization-keyword'),
    path('logout/', Logout.as_view(),  name='logout')
    ]