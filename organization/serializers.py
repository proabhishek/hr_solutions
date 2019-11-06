from rest_framework import serializers
from .models import OrganizationSetUp


class OrganizationSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetUp
        fields = ['id', 'organization_email', 'password', 'auth-token', 'company_name']


class OrganizationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetUp
        fields = ['id', 'logo_url', 'tagline', 'pan_link', 'contact_number', 'office_address']


class TrialSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationSetUp
        fields = ['id', 'is_active']