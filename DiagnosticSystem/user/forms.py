from django import forms
from .models import Patient
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['idcard', 'password']

class PatientCreationForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ['name', 'idcard', 'mobile', 'password1', 'password2']
        labels = {
            'name': '姓名',
            'idcard': '身份证号',
            'mobile': '手机号',
            'password1': '密码',
            'password2': '确认密码',
        }

# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = ['name', 'idcard', 'mobile', 'password1', 'password2']


