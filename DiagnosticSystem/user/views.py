from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, CreateView, FormView
from .models import Patient, Doctor
from .forms import PatientCreationForm, PatientLoginForm
from .forms import DoctorLoginForm
from DiagnosticSystem.mixins import LoginRequiredMixin

# 用户注册
class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientCreationForm
    template_name = 'user/patient_form.html'
    # 用户注册成功 转跳到登陆页面
    success_url = '/user/login/'

# 用户登录
class PatientLoginView(FormView):
    template_name = 'user/patient_login.html'  # 登录页面模板
    form_class = PatientLoginForm         # 使用的表单类

    def form_valid(self, form):
        # 获取表单中的身份证号和密码
        idcard = form.cleaned_data['idcard']
        password = form.cleaned_data['password']

        try:
            # 验证用户是否存在
            patient = Patient.objects.get(idcard=idcard)
            # 检查密码是否匹配
            if patient.check_password(password):
                # 登录成功，将用户信息存入 session
                self.request.session['patient_id'] = patient.id
                self.request.session['patient_name'] = patient.name
                # 跳转到登录后页面
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                # 密码错误
                form.add_error(None, '密码错误，请重新输入')
                return self.form_invalid(form)
        except Patient.DoesNotExist:
            # 用户不存在
            form.add_error(None, '身份证号不存在，请检查后重试')
            return self.form_invalid(form)

# 用户主页
class PatientHomeView(TemplateView):
    template_name = 'user/patient_home.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['patient_name'] = self.request.session.get('patient_name', '游客')
    #     return context
    def get(self, request):
        patient_id = request.session.get('patient_id')
        if patient_id:
            patient = Patient.objects.get(id=patient_id)
        else:
            patient = None
        return render(request, 'user/patient_home.html', {'patient': patient})

# 用户注销
def PatientLogout(request):
    # 清除会话
    request.session.flush()
    # return HttpResponseRedirect(reverse('user_login'))
    return HttpResponseRedirect(reverse('home'))

# 皮肤病介绍
class DiseaseViewForUser(TemplateView):
    template_name = 'user/disease_intro_for_users.html'

class AKIECView(LoginRequiredMixin, TemplateView):
    template_name = 'user/success.html'
    def get(self, request, *args, **kwargs):
        # 检查是否是 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'authenticated'})
        return super().get(request, *args, **kwargs)
class BCCView(LoginRequiredMixin, TemplateView):
    template_name = 'user/success.html'
    def get(self, request, *args, **kwargs):
        # 检查是否是 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'authenticated'})
        return super().get(request, *args, **kwargs)
class BKLView(LoginRequiredMixin, TemplateView):
    template_name = 'user/success.html'
    def get(self, request, *args, **kwargs):
        # 检查是否是 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'authenticated'})
        return super().get(request, *args, **kwargs)
class DFView(LoginRequiredMixin, TemplateView):
    template_name = 'user/success.html'
    def get(self, request, *args, **kwargs):
        # 检查是否是 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'authenticated'})
        return super().get(request, *args, **kwargs)
class NVView(LoginRequiredMixin, TemplateView):
    template_name = 'user/success.html'
    def get(self, request, *args, **kwargs):
        # 检查是否是 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'authenticated'})
        return super().get(request, *args, **kwargs)
class MELView(LoginRequiredMixin, TemplateView):
    template_name = 'user/success.html'
    def get(self, request, *args, **kwargs):
        # 检查是否是 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'authenticated'})
        return super().get(request, *args, **kwargs)
class VASCView(LoginRequiredMixin, TemplateView):
    template_name = 'user/success.html'
    def get(self, request, *args, **kwargs):
        # 检查是否是 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'authenticated'})
        return super().get(request, *args, **kwargs)

# 医生登录
class DoctorLoginView(FormView):
    template_name = 'doctor/doctor_login.html'  # 登录页面模板
    form_class = DoctorLoginForm         # 使用的表单类

    def form_valid(self, form):
        # 获取表单中的编号和密码
        idcard = form.cleaned_data['idcard']
        password = form.cleaned_data['password']
        # print(idcard, password)
        try:
            # 验证用户是否存在
            doctor = Doctor.objects.get(docID=idcard)
            # 检查密码是否匹配
            if doctor.check_password(password):
                # 登录成功，将用户信息存入 session
                self.request.session['doctor_id'] = doctor.docID
                self.request.session['doctor_name'] = doctor.name
                # 跳转到登录后页面
                return HttpResponseRedirect(reverse('doctor_home'))
            else:
                # 密码错误
                form.add_error(None, '密码错误，请重新输入')
                return self.form_invalid(form)
        except Patient.DoesNotExist:
            # 用户不存在
            form.add_error(None, '医生编号不存在，请检查后重试')
            return self.form_invalid(form)

class DoctorHomeView(TemplateView):
    template_name = 'doctor/doctor_home.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['patient_name'] = self.request.session.get('patient_name', '游客')
    #     return context
    def get(self, request):
        doctor_id = request.session.get('doctor_id')
        if doctor_id:
            doctor = Doctor.objects.get(docID=doctor_id)
        else:
            doctor = None
        return render(request, 'doctor/doctor_home.html', {'doctor': doctor})

