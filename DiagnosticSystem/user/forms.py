from django import forms
from .models import Patient

class PatientCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="密码", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = Patient
        fields = ['idcard', 'name', 'gender', 'mobile', 'email']  # 包括患者相关的字段

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # 确保两个密码字段匹配
        if password1 != password2:
            raise forms.ValidationError("密码和确认密码不匹配")
        return password2

    def save(self, commit=True):
        patient = super().save(commit=False)  # 获取患者对象
        patient.set_password(self.cleaned_data["password1"])  # 加密密码
        if commit:
            patient.save()  # 保存患者对象
        return patient

class PatientLoginForm(forms.Form):
    idcard = forms.CharField(
        max_length=20, 
        required=True, 
        label='身份证号',
        widget=forms.TextInput(attrs={'placeholder': '请输入身份证号'})
    )
    password = forms.CharField(
        max_length=128, 
        required=True, 
        label='密码',
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'})
    )

from django.core.validators import RegexValidator

class PatientForm(forms.ModelForm):
    mobile = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message='请输入有效的11位手机号码'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '^1[3-9]\\d{9}$',
            'title': '请输入有效的11位手机号码'
        })
    )

    class Meta:
        model = Patient
        fields = ['idcard', 'name', 'gender', 'mobile', 'email', 'avatar']
        widgets = {
            'idcard': forms.TextInput(attrs={'readonly': True, 'class': 'form-control bg-light'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('M', '男'),
                ('F', '女'),
            ]),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'avatarUpload',
            }),
        }
        labels = {
            'idcard': '身份证号',
            'name': '姓名',
            'gender': '性别',
            'mobile': '手机号',
            'email': '电子邮箱',
            'avatar': '头像'
        }

class DoctorLoginForm(forms.Form):
    idcard = forms.CharField(
        max_length=20, 
        required=True, 
        label='编号',
        widget=forms.TextInput(attrs={'placeholder': '请输入编号'})
    )
    password = forms.CharField(
        max_length=128, 
        required=True, 
        label='密码',
        widget=forms.PasswordInput(attrs={'placeholder': '请输入密码'})
    )


