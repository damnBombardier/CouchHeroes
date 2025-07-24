# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import PlayerProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = PlayerProfile
        fields = ['bio'] # Поля профиля для редактирования

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile
