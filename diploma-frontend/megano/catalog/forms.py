from django import forms
from django.contrib.auth.forms import UserCreationForm
from myauth.models import Profile
from django.contrib.auth.models import User


class CustomUserCreationAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)


class CreateUserForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("first_name", "username", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["name"]
        if commit:
            user.save()
        return user
