# from django.db import models
# # from datetime import datetime
# from django.contrib.auth.models import User

# class Patient(models.Model):
#     # 定义一个关联模型，存储与普通用户相关的信息
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # 其他字段
#     gender_choices = (
#         ('male','男'),
#         ('female','女')
#     )
#     idcard = models.CharField('身份证号',max_length=20, blank=True, unique=True)
#     name = models.CharField('姓名',max_length=50, blank=True)
#     mobile = models.CharField('手机号',max_length=11, blank=True)
#     gender = models.CharField('性别',max_length=10,choices=gender_choices)
#     # image = models.ImageField(upload_to='image/%Y%m',default='image/default.png',max_length=100)

#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name = '患者'
#         verbose_name_plural = verbose_name
        

from django.db import models
from django.contrib.auth.hashers import make_password  # 用于密码加密

class Patient(models.Model):
    
    idcard = models.CharField('身份证号', max_length=20, blank=True, unique=True)
    name = models.CharField('姓名', max_length=50, blank=True)
    mobile = models.CharField('手机号', max_length=11, blank=True)
    gender = models.CharField('性别', max_length=10, choices=[('M', '男'), ('F', '女')])
    password = models.CharField('密码', max_length=128)  # 存储加密后的密码

    def set_password(self, raw_password):
        """加密密码并保存"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """检查密码是否匹配"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.idcard})"
    
    class Meta:
        verbose_name = '患者'
        verbose_name_plural = verbose_name


'''
# 性别选择项
gender_choices = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

class User(AbstractUser):
    # 添加 is_staff 字段，用来区分是否可以访问后台
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)  # 用于区分是否是医生

class Patient(models.Model):
    # 定义一个关联模型，存储与普通用户相关的信息
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    # 其他
    idcard = models.CharField('身份证号', max_length=20, blank=True, unique=True)
    name = models.CharField('姓名', max_length=50, blank=True)
    mobile = models.CharField('手机号', max_length=11, blank=True)
    gender = models.CharField('性别', max_length=10, choices=gender_choices)
    
    def __str__(self):
        return f"{self.name} ({self.idcard})"

    class Meta:
        verbose_name = '患者'
        verbose_name_plural = verbose_name



class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')  # 关联User模型
    name = models.CharField('姓名', max_length=50)
    title = models.CharField('职称', max_length=50)  # 职称，如：主任医师、副主任医师等
    department = models.CharField('科室', max_length=100)  # 科室，如：内科、外科等
    mobile = models.CharField('手机号', max_length=11, blank=True)
    gender = models.CharField('性别', max_length=10, choices=gender_choices)

    def __str__(self):
        return f"Dr. {self.name} ({self.title})"

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        '''

    