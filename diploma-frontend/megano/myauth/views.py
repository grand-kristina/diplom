import json

from django.db import transaction
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User

from .models import Profile, Avatar
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
)


class SignInView(APIView):
    def post(self, request: Request) -> Response:
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    @transaction.atomic
    def post(self, request: Request) -> Response:
        data = list(request.data.keys())[0]
        user_data = json.loads(data)
        user_data["profile"] = {
            "fullName": user_data["name"],
        }
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(
                request, username=user_data["username"], password=user_data["password"]
            )
            if user is not None:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request: Request) -> Response:
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request: Request):
        profile = Profile.objects.get(user=request.user)
        serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ProfilePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        current_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")

        if not current_password or not new_password:
            return Response(
                {"error": "Both currentPassword and newPassword are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        if not user.check_password(current_password):
            return Response(
                {"error": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_200_OK)


class ProfileAvatarView(APIView):
    def post(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user)
        default_size_image = 2 * 1024 * 1024
        avatar_file = request.FILES["avatar"]
        if avatar_file.size == default_size_image:
            if profile.avatar:
                profile.avatar.src = avatar_file
                profile.avatar.save()
            else:
                avatar = Avatar.objects.create(src=avatar_file, alt="User Avatar")
                profile.avatar = avatar
                profile.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
