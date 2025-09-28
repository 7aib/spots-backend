import secrets

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import UserProfile
from accounts.utils import get_age_group


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "password_confirm",
            "dob",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def validate_username(self, value):
        if UserProfile.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = UserProfile.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            dob=validated_data.pop("dob", None),
            age_group=get_age_group(self, validated_data.get('dob')),
        )
        # Create token for the user
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include username and password")


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data"""

    class Meta:
        model = UserProfile
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            UserProfile.objects.get(email=value)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def validate_uid(self, value):
        try:
            uid = force_str(urlsafe_base64_decode(value))
            user = UserProfile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link")
        return value

    def validate_token(self, value):
        try:
            uid = force_str(urlsafe_base64_decode(self.initial_data.get("uid")))
            user = UserProfile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
            raise serializers.ValidationError("Invalid reset link")

        if not default_token_generator.check_token(user, value):
            raise serializers.ValidationError("Invalid or expired reset link")
        return value
