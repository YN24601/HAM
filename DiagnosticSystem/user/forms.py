from django import forms
from .models import Patient, Doctor, DoctorSchedule, Appointment, AppointmentStatus, MedicalRecord
from django.core.validators import RegexValidator

class PatientCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        help_text="至少8个字符"
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    sms_code = forms.CharField(
        label='短信验证码',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入6位验证码'}),
        max_length=6
    )

    class Meta:
        model = Patient
        fields = ['idcard', 'name', 'gender', 'mobile', 'email']
        widgets = {
            'idcard': forms.TextInput(attrs={'class': 'form-control', 'pattern': '\d{17}[\dXx]'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'pattern': '1[3-9]\d{9}'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
        }
        help_texts = {
            'idcard': '请输入18位有效身份证号码',
            # 'mobile': '用于登录和接收验证码',
            # 'email': '用于找回密码和重要通知',
        }
    
    sms_code = forms.CharField(label='短信验证码', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # gender_choices = [
        #     ('M', '男'),
        #     ('F', '女'),
        # ]
        self.fields['gender'].choices = [('M', '男'), ('F', '女')]
    
    def clean_idcard(self):
        idcard = self.cleaned_data.get('idcard')
        if len(idcard) != 18:
            raise forms.ValidationError("身份证号必须为18位")
        if not idcard[:-1].isdigit():
            raise forms.ValidationError("前17位必须为数字")
        if Patient.objects.filter(idcard=idcard).exists():
            raise forms.ValidationError("该身份证号已注册")
        return idcard.upper()

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if Patient.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("该手机号已注册")
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Patient.objects.filter(email=email).exists():
            raise forms.ValidationError("该邮箱已被使用")
        return email

    def clean(self):
        cleaned_data = super().clean()
        mobile = cleaned_data.get('mobile')
        sms_code = cleaned_data.get('sms_code')
        print("mobile: ", mobile)
        print("sms_code: ", sms_code)
        
        # 验证短信验证码
        session_code = self.request.session.get('sms_verification_code')
        session_mobile = self.request.session.get('sms_mobile')

        if not session_code or not session_mobile:
            raise forms.ValidationError('请先获取短信验证码')

        if mobile != session_mobile:
            raise forms.ValidationError('手机号与接收验证码的手机号不一致')

        if sms_code != session_code:
            raise forms.ValidationError('验证码错误')

        # 验证成功后清除session
        del self.request.session['sms_verification_code']
        del self.request.session['sms_mobile']
        return cleaned_data

    def clean_password2(self):
        # 保持原有的密码验证逻辑
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("密码和确认密码不匹配")
        return password2

    def save(self, commit=True):
        patient = super().save(commit=False)
        patient.set_password(self.cleaned_data["password1"])
        if commit:
            patient.save()
        print(patient)
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
            # 'gender': forms.Select(attrs={'class': 'form-control bg-light', 'disabled': True}, choices=[
            #     ('M', '男'),
            #     ('F', '女'),
            # ]),
            'gender': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('M', '男'),
                ('F', '女'),
            ]),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                # 'id': 'avatarUpload',
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

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['docID', 'name', 'gender', 'title', 'email', 'birthday', 'avatar', 'intro']
        widgets = {
            'docID': forms.TextInput(attrs={'readonly': True, 'class': 'form-control bg-light'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'gender': forms.Select(attrs={'class': 'form-control bg-light', 'disabled': True}, choices=[
            #     ('M', '男'),
            #     ('F', '女'),
            # ]),
            'gender': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('M', '男'),
                ('F', '女'),
            ]),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                # 'id': 'avatarUpload',
            }),
            'intro': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'docID': '医生编号',
            'name': '姓名',
            'gender': '性别',
            'title': '职称',
            'email': '电子邮箱',
            'birthday': '出生日期',
            'avatar': '头像',
            'intro': '简介',
        }

# create shchedule
class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['date', 'start_time', 'end_time', 'max_patients']

gender_choices = [
    ('', '不限'), 
    ('M', '男'),
    ('F', '女'),
]

class DoctorFilterForm(forms.Form):
    name = forms.CharField(label='姓名', required=False)
    title = forms.CharField(label='职称', required=False)
    gender = forms.ChoiceField(label='性别', choices=gender_choices, required=False)
    min_age = forms.IntegerField(label='最小年龄', required=False)
    max_age = forms.IntegerField(label='最大年龄', required=False)

    # 排序选项
    SORT_CHOICES = [
        ('', '默认排序'),
        ('name', '姓名升序'),
        ('-name', '姓名降序'),
        ('title', '职称升序'),
        ('-title', '职称降序'),
        ('birthday', '年龄升序'),
        ('-birthday', '年龄降序'),
    ]
    sort_by = forms.ChoiceField(label='排序方式', choices=SORT_CHOICES, required=False)

class ScheduleFilterForm(forms.Form):
    name = forms.CharField(label='姓名', required=False)
    gender = forms.ChoiceField(label='性别', choices=gender_choices, required=False)
    title = forms.CharField(label='职称', required=False)
    # min_age = forms.IntegerField(label='最小年龄', required=False)
    # max_age = forms.IntegerField(label='最大年龄', required=False)
    date = forms.DateField(label='日期', required=False)
    time = forms.TimeField(label='时间', required=False)

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['image', 'diagnosis', 'treatment']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'onchange': 'previewImage(event)',
            }),
            'diagnosis': forms.Textarea(attrs={'rows': 4, 'placeholder': '请输入诊断结论...', 'class':"form-control" }),
            'treatment': forms.Textarea(attrs={'rows': 4, 'placeholder': '请输入治疗方案...', 'class':"form-control"}),
        }
        labels = {
            'image': '病灶图片',
            'diagnosis': '临床诊断',
            'treatment': '治疗方案',
        }
