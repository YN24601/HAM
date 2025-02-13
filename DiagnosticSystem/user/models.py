from django.db import models
from django.contrib.auth.hashers import make_password  # 用于密码加密
from django.core.validators import RegexValidator
from datetime import datetime, timezone

gender_choices = [
    ('M', '男'),
    ('F', '女'),
]

class Patient(models.Model):
    idcard = models.CharField('身份证号', max_length=20, blank=False, null=False, unique=True)
    name = models.CharField('姓名', max_length=50, blank=False)
    gender = models.CharField('性别', max_length=10, choices=gender_choices)
    mobile = models.CharField('手机号', max_length=11, blank=False, unique=True,
        validators=[RegexValidator(regex='^[0-9]{11}$', message='手机号必须为11位数字')])
    email = models.EmailField('邮箱', max_length=100, unique=True)    
    password = models.CharField('密码', max_length=128)  # 加密后的密码
    # avatar = models.CharField('头像', max_length=100, default='static/images/default_user.jpg')
    avatar = models.ImageField('头像', upload_to='avatars/patients/', default='avatars/patients/default_patient.jpg')
    # avatar = models.CharField('头像', max_length=100, default='/Users/yanazhang/Documents/vscodeProjects/pythonProjects/HAM/DiagnosticSystem/static/images/default_user.jpg')
    created_at = models.DateTimeField('创建时间', auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)

    def set_password(self, raw_password):
        """加密密码并保存"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """检查密码是否匹配"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def getBirthday(self):
        """根据身份证号获取出生日期"""
        if self.idcard and len(self.idcard) >= 14:
            # 身份证号的第7到14位是出生日期
            birthday_str = self.idcard[6:14]
            try:
                # 将字符串转换为日期对象
                birthday = datetime.strptime(birthday_str, "%Y%m%d").date()
                return birthday
            except ValueError:
                # 如果日期格式不正确，返回None
                return None
        return None

    def getAge(self):
        """根据身份证号获取年龄"""
        birthday = self.getBirthday()
        if birthday:
            today = datetime.today().date()
            age = today.year - birthday.year
            # 如果今年生日还没过，年龄减一
            if (today.month, today.day) < (birthday.month, birthday.day):
                age -= 1
            return age
        return None

    def __str__(self):
        return f"{self.name} ({self.idcard})"
    
    class Meta:
        verbose_name = '患者'
        verbose_name_plural = verbose_name



class Doctor(models.Model):
    docID = models.CharField('医生编号', max_length=20, unique=True, null=False, blank=False)
    name = models.CharField('姓名', max_length=50, blank=False)
    title = models.CharField('职称', max_length=50)
    gender = models.CharField('性别', max_length=10, choices=gender_choices)
    birthday = models.DateField('出生日期', null=True, blank=True)
    email = models.EmailField('邮箱', max_length=100, unique=True, blank=False)
    intro = models.TextField('简介', max_length=500, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/doctors/', default='avatars/doctors/default_doctor.jpg')
    password = models.CharField('密码', max_length=128, default='password')
    created_at = models.DateTimeField('创建时间', auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)

    def set_password(self, raw_password):
        """加密密码并保存"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """检查密码是否匹配"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"Dr. {self.name} ({self.title})"

    class Meta:
        verbose_name = '医生'
        verbose_name_plural = verbose_name
