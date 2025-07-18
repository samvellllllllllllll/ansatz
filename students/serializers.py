from rest_framework import serializers
from .models import CustomUser, ConfirmationCode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
    
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Введите корректный email адрес.")
        
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже зарегистрирован.")
        
        return value
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ConfirmationCodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = ConfirmationCode
        fields = ('email', 'code')