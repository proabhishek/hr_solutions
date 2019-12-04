from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(OrganizationSetUp)
admin.site.register(CompanyVerification)
admin.site.register(CompanyContactExtra)
admin.site.register(CompanyAddress)

