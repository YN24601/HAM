from django.db import models
# from datetime import datetime
from django.contrib.auth.models import AbstractUser


class Patient(AbstractUser):
    # 去掉用不上的继承属性
    
    gender_choices = (
        ('male','男'),
        ('female','女')
    )
    idcard = models.CharField('身份证号',max_length=20, blank=True, unique=True)
    name = models.CharField('姓名',max_length=50, blank=True)
    mobile = models.CharField('手机号',max_length=11, blank=True)
    gender = models.CharField('性别',max_length=10,choices=gender_choices)
    # image = models.ImageField(upload_to='image/%Y%m',default='image/default.png',max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '患者'
        verbose_name_plural = verbose_name
        
    
        



    