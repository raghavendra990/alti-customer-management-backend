

from rest_framework.serializers import (
    Serializer, ModelSerializer, SerializerMethodField, UUIDField,
    CharField, ChoiceField, EmailField, BooleanField, ListField, JSONField, IntegerField, DateField, DateTimeField)

from phonenumber_field.serializerfields import PhoneNumberField
from .models import UserModel, Plan
from django.utils import timezone
from .models import STATUS_CHOICE
class RegisterSerializer(Serializer):  # pylint: disable=abstract-method
    """
    Register serializer
    """
    name = CharField(max_length=50,  required=True, trim_whitespace=True)
    email = EmailField(max_length=50,  required=True, trim_whitespace=True)
    password = CharField(max_length=16,  required=True)
    adhar_number = CharField(max_length=12, min_length=12, required=True, trim_whitespace=True)
    dob = DateField(required=True)
    phone_number = PhoneNumberField(required=True, trim_whitespace=True)
    registration_date = DateTimeField(default=timezone.now)
    plan = CharField(max_length=50,  required=True, trim_whitespace=True)
    # expiry = DateField(required=True)
    # plan_status = ChoiceField(choices=STATUS_CHOICE, default='inactive',  required=False)

class PlanSerializer(ModelSerializer):  # pylint: disable=abstract-method
    """
    Register serializer
    """
    class Meta:
        model = Plan
        fields = ('id', 'name', 'price', 'validity', 'status')
   
class LoginSerializer(Serializer):  # pylint: disable=abstract-method
    """
    Login serializer
    """
    email = EmailField(required=True, trim_whitespace=True)
    password = CharField(max_length=16,  required=True)

    
class UserDetailsSerializer(ModelSerializer):  # pylint: disable=abstract-method
    """
    UserDetails serializer
    """
    class Meta:
        model = UserModel
        fields = ('id', 'name', 'email', 'adhar_number', 'phone_number', 'dob', 'plan', 'expiry', 'plan_status', 'registration_date')
   
class UpgradeDowngradeSerializer(Serializer):  # pylint: disable=abstract-method
    """
    Login serializer
    """
    id = UUIDField(required=True)
