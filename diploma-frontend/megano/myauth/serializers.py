from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Avatar, Profile


class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class UpdateProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", required=False)

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        email = user_data.get("email")

        if email:
            instance.user.email = email
            instance.user.save()

        instance.fullName = validated_data.get("fullName", instance.fullName)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True)
    email = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]

    @staticmethod
    def get_email(obj):
        return obj.user.email


class CreateProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(required=False)

    class Meta:
        model = Profile
        fields = ["fullName", "phone", "avatar"]

    def create(self, validated_data):
        avatar_data = validated_data.pop("avatar", None)
        if avatar_data:
            avatar = Avatar.objects.create(**avatar_data)
            profile = Profile.objects.create(avatar=avatar, **validated_data)
        else:
            profile = Profile.objects.create(**validated_data)
        return profile


class UserSerializer(serializers.ModelSerializer):
    profile = CreateProfileSerializer()

    class Meta:
        model = User
        fields = ["username", "password", "profile"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user
