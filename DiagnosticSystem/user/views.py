from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView
from .models import Patient
from .forms import PatientCreationForm


class PatientCreateView(CreateView):
    
    form_class = PatientCreationForm
    template_name = 'user/patient_form.html'
    
    # 用户注册成功 转跳到登陆页面