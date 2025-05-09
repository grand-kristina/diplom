from django.urls import path

from .views import (
    SignInView,
    SignUpView,
    signOut,
    ProfileView,
    ProfilePasswordView,
    ProfileAvatarView,
)

app_name = "myauth"

urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("sign-out/", signOut, name="sign-out"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/password/", ProfilePasswordView.as_view(), name="change_password"),
    path("profile/avatar/", ProfileAvatarView.as_view(), name="change_avatar"),
]
