from django.db import models
import uuid

# Create your models here.


class OrganizationSetUp(models.Model):
    company_name = models.CharField(max_length=200, blank=True, null=True)
    logo_url = models.CharField(max_length=500, blank=True, null=True)
    tagline = models.TextField(blank=True, null=True)
    pan_link = models.CharField(max_length=500, blank=True, null=True)
    organization_email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=13, blank=True, null=True)
    office_address = models.TextField(blank=True, null=True)
    otp = models.PositiveIntegerField(null=True, blank=True)
    otp_sent_at = models.DateTimeField(blank=True, null=True)
    company_keyword = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    auth_token = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-id']
        db_table = 'Organization'
