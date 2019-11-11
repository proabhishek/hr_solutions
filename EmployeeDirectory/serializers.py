from rest_framework import serializers
from .models import *


class UpdateEmployeeSerializer(serializers.Serializer):
    class Meta:
        model = Employee
        fields = '__all__'
