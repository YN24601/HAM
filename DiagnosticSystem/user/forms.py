from django import forms
from .models import Patient

class PatientCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="密码", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = Patient
        fields = ['idcard', 'name', 'mobile', 'gender']  # 包括患者相关的字段

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




'''

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
        model = User  # 使用 User 模型而不是 Patient
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': '用户名',
            'password1': '密码',
            'password2': '确认密码',
        }
        
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # 添加errors属性


    def save(self, commit=True):
        # 首先保存 User 实例
        user = super().save(commit=False)
        if commit:
            user.save()

        # 然后创建关联的 Patient 实例
        patient = Patient.objects.create(
            user=user,
            name=self.cleaned_data.get('name'),
            idcard=self.cleaned_data.get('idcard'),
            mobile=self.cleaned_data.get('mobile'),
            gender=self.cleaned_data.get('gender')
        )
        return patient

'''


