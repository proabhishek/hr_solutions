from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=50)
    employee_number = models.CharField(max_length=12)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    pic_url = models.CharField(max_length=1000)
    pan_card_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=13)
    package = models.IntegerField()
    salary = models.FloatField()
    date_of_birth = models.CharField(max_length=11)
    date_of_joining = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
