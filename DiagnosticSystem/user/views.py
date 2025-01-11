from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView
from .models import User

class UserCreateView(CreateView):
    model = User
    fields = '__all__'
    
    # 用户注册成功 转跳到登陆页面