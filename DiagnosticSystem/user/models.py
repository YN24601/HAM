from django.db import models
from datetime import datetime

class User(models.Model):
    gender_choices = (
        ('male','男'),
        ('female','女')
    )
    idcard = models.CharField('身份证号',max_length=20,null=True,blank=True, unique=True)
    name = models.CharField('姓名',max_length=50)
    mobile = models.CharField('手机号',max_length=11,null=True,blank=True)
    email = models.EmailField('邮箱',max_length=50,unique=True)
    birthday = models.DateField('生日',null=True,blank=True)
    gender = models.CharField('性别',max_length=10,choices=gender_choices)
    # image = models.ImageField(upload_to='image/%Y%m',default='image/default.png',max_length=100)

    def __str__(self):
        return self.name



    