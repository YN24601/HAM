from django import forms
from .models import UserProfile

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['idcard', 'password']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


