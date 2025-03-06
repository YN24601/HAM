from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, CreateView, FormView, UpdateView
from .models import Patient, Doctor, DoctorSchedule
from .forms import PatientCreationForm, PatientLoginForm, PatientForm
from .forms import DoctorLoginForm, DoctorForm, DoctorScheduleForm
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
    def get(self, request):
        # 获取当前用户的patient_id
        patient_id = request.session.get('patient_id')
        # 如果存在patient_id，则获取对应的patient对象
        if patient_id:
            patient = Patient.objects.get(id=patient_id)
        # 否则，将patient设置为None
        else:
            patient = None
        # 渲染模板，并将patient对象传递给模板
        return render(request, 'user/patient_home.html', {'patient': patient})

# 用户注销
def PatientLogout(request):
    # 清除会话
    request.session.flush()
    # return HttpResponseRedirect(reverse('user_login'))
    return HttpResponseRedirect(reverse('home'))

# PatientProfileView
class PatientProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'user/patient_profile.html'
    form_class = PatientForm
    
    def get_object(self):
        patient_id = self.request.session.get('patient_id')
        return Patient.objects.get(id=patient_id)
    
    def get_success_url(self):
        return reverse('patient_profile') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # patient_id = self.request.session.get('patient_id')
        # patient = Patient.objects.get(id=patient_id)
        context['patient'] = self.object
        return context
    # def form_valid(self, form):
    #     print('上传的文件:', self.request.FILES)  # 检查文件是否上传
    #     print('表单数据:', form.cleaned_data)    # 检查处理后的数据
    #     return super().form_valid(form)

# 皮肤病介绍
class DiseaseViewForUser(TemplateView):
    template_name = 'user/disease_intro_for_users.html'

    def get(self, request):
        # 获取当前用户的patient_id
        patient_id = request.session.get('patient_id')
        # 如果存在patient_id，则获取对应的patient对象
        if patient_id:
            patient = Patient.objects.get(id=patient_id)
        else:
            patient = None
        return render(request, 'user/disease_intro_for_users.html', {'patient': patient})

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

class DoctorIntroView(TemplateView):
    template_name = 'user/doctor_intro.html'
    def get(self, request):
        # 获取当前用户的patient_id
        patient_id = request.session.get('patient_id')
        # 如果存在patient_id，则获取对应的patient对象
        if patient_id:
            patient = Patient.objects.get(id=patient_id)
        else:
            patient = None
        return render(request, 'user/doctor_intro.html', {'patient': patient})

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
                self.request.session['doctor_id'] = doctor.id
                self.request.session['doctor_name'] = doctor.name
                # print(doctor.id, doctor.docID, doctor.name )
                # 跳转到登录后页面
                return HttpResponseRedirect(reverse('doctor_home'))
            else:
                # 密码错误
                form.add_error(None, '密码错误，请重新输入')
                return self.form_invalid(form)
        except Doctor.DoesNotExist:
            # 用户不存在
            form.add_error(None, '医生编号不存在，请检查后重试')
            return self.form_invalid(form)

class DoctorHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'doctor/doctor_home.html'
    def get(self, request):
        doctor_id = request.session.get('doctor_id')
        doctor = Doctor.objects.get(id=doctor_id)
        return render(request, 'doctor/doctor_home.html', {'doctor': doctor})

# 用户注销
def DoctorLogout(request):
    # 清除会话
    request.session.flush()
    # return HttpResponseRedirect(reverse('user_login'))
    return HttpResponseRedirect(reverse('home'))
    
class DoctorProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'doctor/doctor_profile.html'
    form_class = DoctorForm
    
    def get_object(self):
        doctor_id = self.request.session.get('doctor_id')
        return Doctor.objects.get(id=doctor_id)
    
    def get_success_url(self):
        return reverse('doctor_profile') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = self.object
        return context


class DoctorScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'doctor/doctor_schedule.html'

    def get(self, request):
        doctor_id = request.session.get('doctor_id')
        doctor = Doctor.objects.get(id=doctor_id)
        
        # 处理筛选条件
        available = request.GET.get('available')
        if available is not None:
            available = int(available)
            schedules = DoctorSchedule.objects.filter(doctor=doctor, is_available=available).order_by('date', 'start_time')
        else:
            schedules = DoctorSchedule.objects.filter(doctor=doctor).order_by('date', 'start_time')
        
        # 创建表单实例
        form = DoctorScheduleForm()
        
        return render(request, self.template_name, {
            'schedules': schedules,
            'doctor': doctor,
            'form': form
        })

    def post(self, request):
        doctor_id = request.session.get('doctor_id')
        doctor = Doctor.objects.get(id=doctor_id)
        
        form = DoctorScheduleForm(request.POST)
        print('form:', form)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.doctor = doctor
            schedule.save()
            return redirect('doctor_schedule')
        
        # 如果表单无效，重新渲染页面并显示错误信息
        schedules = DoctorSchedule.objects.filter(doctor=doctor).order_by('date', 'start_time')
        # print('schedules:', schedules)
        return render(request, self.template_name, {
            'schedules': schedules,
            'doctor': doctor,
            'form': form
        })


from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from .models import DoctorSchedule
from .forms import DoctorScheduleForm

class DoctorScheduleEditView(LoginRequiredMixin, UpdateView):
    model = DoctorSchedule
    form_class = DoctorScheduleForm
    template_name = 'doctor/doctor_schedule_edit.html'
    context_object_name = 'schedule'
    success_url = reverse_lazy('doctor_schedule')

    def form_valid(self, form):
        schedule = form.instance
        # 检查 max_patients 是否小于已预约的患者人数
        if form.cleaned_data['max_patients'] < schedule.current_patients:
            form.add_error('max_patients', '最大患者数不能小于已预约的患者人数')
            return self.form_invalid(form)
        return super().form_valid(form)

def DoctorScheduleDelete(request, pk):
    schedule = DoctorSchedule.objects.get(id=pk)
    schedule.delete()
    return redirect('doctor_schedule')