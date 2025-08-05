from rest_framework import serializers
from django.db import transaction
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "phone_number",
            "first_name",
            "middle_name",
            "last_name",
            "birth_date",
            "address",
            "profile_picture",
            "qr_code",
        )

        def update(self, instance, validated_data):
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "username",
            "password",
            "phone_number",
            "birth_date",
            "address",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "profile_picture": {"required": False},
        }

        def create(self, validated_data):
            first_name = validated_data.get("first_name", None)
            middle_name = validated_data.get("middle_name", None)
            last_name = validated_data.get("last_name", None)
            email = validated_data.get("email")
            username = validated_data.get("username")
            password = validated_data.get("password")
            phone_number = validated_data.get("phone_number", None)
            birth_date = validated_data.get("birth_date", None)
            address = validated_data.get("address", None)

            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    password=password,
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    birth_date=birth_date,
                    address=address,
                )
            return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, required=True, allow_blank=False)

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if email is None and password is None:
            raise serializers.ValidationError(
                "Email and password are required to log in."
            )

        try:
            user: User = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        if user.check_password(password):
            attrs["user"] = user
        else:
            attrs["user"] = None
            raise serializers.ValidationError("Incorrect password.")
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        max_length=255 * 2, required=True, allow_blank=False
    )
