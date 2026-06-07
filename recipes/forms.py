from django import forms
from django.contrib.auth.models import User
from .models import Profile


# Форма реєстрації користувача
class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label="Логін")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ["username", "email", "password"]


# Форма редагування спортивного профілю
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "height", "weight", "sport_type", "daily_calories"]
        labels = {
            "height": "Ріст (см)",
            "weight": "Вага (кг)",
            "sport_type": "Вид спорту / Напрямок",
            "daily_calories": "Цільовий калораж на день",
        }
