from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView
from .models import Patient
from .forms import PatientCreationForm

from django.shortcuts import render, redirect
from .forms import PatientCreationForm

# def create_patient(request):
#     if request.method == 'POST':
#         form = PatientCreationForm(request.POST)
#         if form.is_valid():
#             form.save()  # 保存患者对象，密码会被加密存储
#             return redirect('success_url')  # 创建成功后跳转
#     else:
#         form = PatientCreationForm()

#     return render(request, 'create_patient.html', {'form': form})

class PatientCreateView(CreateView):
    
    model = Patient
    form_class = PatientCreationForm
    template_name = 'user/patient_form.html'
    
    # 用户注册成功 转跳到登陆页面
    success_url = '/user/login/'

def PatientLoginView(request):
    return render(request, 'user/patient_login.html')