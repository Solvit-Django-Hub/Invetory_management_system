from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "role",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(
        write_only=True,
        required=False
    )

    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=False
    )

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "old_password",
            "new_password",
        ]

    def validate_email(self, value):
        user = self.instance

        if User.objects.exclude(
            user_id=user.user_id
        ).filter(email=value).exists():

            raise serializers.ValidationError(
                "This email is already in use."
            )

        return value

    def validate(self, data):
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if new_password and not old_password:
            raise serializers.ValidationError({
                "old_password": "Old password is required."
            })

        if old_password and not new_password:
            raise serializers.ValidationError({
                "new_password": "New password is required."
            })

        if old_password and not self.instance.check_password(old_password):
            raise serializers.ValidationError({
                "old_password": "Old password is incorrect."
            })

        return data

    def update(self, instance, validated_data):
        old_password = validated_data.pop("old_password", None)
        new_password = validated_data.pop("new_password", None)

        instance.name = validated_data.get(
            "name",
            instance.name
        )

        instance.email = validated_data.get(
            "email",
            instance.email
        )

        if new_password:
            instance.set_password(new_password)

        instance.save()

        return instance

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "user_id",
            "name",
            "email",
            "role",
        ]