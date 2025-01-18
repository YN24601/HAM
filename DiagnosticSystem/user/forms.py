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



