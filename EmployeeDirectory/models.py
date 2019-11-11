from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=12)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    pan_card_number = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=13, null=True, blank=True)
    date_of_birth = models.CharField(max_length=11, null=True, blank=True)
    date_of_joining = models.CharField(max_length=11, null=True, blank=True)
    blood_group = models.CharField(max_length=3, null=True, blank=True)
    emergency_contact = models.CharField(max_length=17, null=True, blank=True)
    confirmation_date = models.CharField(max_length=11, null=True, blank=True)
    date_of_exit = models.CharField(max_length=11, null=True, blank=True)
    password = models.CharField(max_length=20)
    auth_token = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


