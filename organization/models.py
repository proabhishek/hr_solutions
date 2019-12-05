from django.db import models
import uuid

# Create your models here.


class OrganizationSetUp(models.Model):
    DOMAIN_TYPE_CHOICE = (
        ('sub-domain', 'Sub Domain'),
        ('custom-domain', 'Custom Domain')
    )
    company_name = models.CharField(max_length=200, blank=True, null=True)
    logo_url = models.CharField(max_length=500, blank=True, null=True)
    pan_number = models.CharField(max_length=500, blank=True, null=True)
    organization_email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=13, blank=True, null=True)
    domain = models.CharField(max_length=100, null=True, blank=True)
    domain_type = models.CharField(choices=DOMAIN_TYPE_CHOICE, max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    auth_token = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-id']
        db_table = 'Organization'


class CompanyAddress(models.Model):
    company = models.ForeignKey(OrganizationSetUp, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.TextField()
    branch_code = models.CharField(max_length=20)
    is_head_office = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-id']
        db_table = 'CompanyAddress'


class CompanyContactExtra(models.Model):
    company = models.ForeignKey(OrganizationSetUp, on_delete=models.CASCADE)
    label = models.CharField(max_length=30)
    label_info = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-id']
        db_table = 'CompanyContactExtra'


class CompanyVerification(models.Model):
    company = models.ForeignKey(OrganizationSetUp, on_delete=models.CASCADE)
    otp = models.PositiveIntegerField(null=True, blank=True)
    otp_sent_at = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(blank=True, null=True)
    otp_verified_at = models.DateTimeField(blank=True, null=True)
    mail_activation_token = models.CharField(max_length=40, null=True, blank=True)
    email_sent_at = models.DateTimeField(blank=True, null=True)
    email_verified = models.BooleanField(blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
        db_table = 'CompanyVerification'


class FreeTrial(models.Model):
    company = models.ForeignKey(OrganizationSetUp, on_delete=models.CASCADE)
    trail_active = models.BooleanField(blank=True, null=True)
    trial_start_date = models.DateTimeField(blank=True, null=True)
    trail_end_date = models.DateTimeField(blank=True, null=True)
    payment_active = models.BooleanField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
        db_table = 'CompanyFreeTrial'


class PaymentPlan(models.Model):
    plan_name = models.CharField(max_length=30)
    plan_code = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']
        db_table = 'CompanyPaymentPlan'




