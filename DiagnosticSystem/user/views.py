from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, ListView, DetailView
from django.db.models import Q
CUSTOM_MESSAGE_LEVEL = 10  # 自定义消息级别
from .models import Patient, Doctor, DoctorSchedule, Appointment, AppointmentStatus, MedicalRecord
from .forms import PatientCreationForm, PatientLoginForm, PatientForm, DoctorFilterForm, ScheduleFilterForm
from .forms import DoctorLoginForm, DoctorForm, DoctorScheduleForm, MedicalRecordForm
from DiagnosticSystem.mixins import LoginRequiredMixin
from datetime import date, timedelta, datetime
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import torch
import torchvision.models as models
from torchvision import transforms
import torch.nn.functional as F
from PIL import Image
import os

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

################## 静态 - 皮肤病介绍 ###################
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

################### 功能 ###################

class DoctorListView(TemplateView):
    template_name = 'user/doctor_list.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        # 获取所有医生
        doctors = Doctor.objects.all()

        # 初始化表单
        form = DoctorFilterForm(self.request.GET or None)

        if form.is_valid():
            # 获取表单数据
            name = form.cleaned_data.get('name')
            title = form.cleaned_data.get('title')
            gender = form.cleaned_data.get('gender')
            min_age = form.cleaned_data.get('min_age')
            max_age = form.cleaned_data.get('max_age')
            sort_by = form.cleaned_data.get('sort_by')

            # 构建查询条件
            query = Q()
            if name:
                query &= Q(name__icontains=name)
            if title:
                query &= Q(title__icontains=title)
            if gender:
                query &= Q(gender=gender)

            # 年龄范围筛选
            if min_age or max_age:
                today = date.today()
                if min_age:
                    max_birthday = today - timedelta(days=min_age * 365)
                    query &= Q(birthday__lte=max_birthday)
                if max_age:
                    min_birthday = today - timedelta(days=(max_age + 1) * 365)
                    query &= Q(birthday__gt=min_birthday)

            # 应用查询条件
            doctors = doctors.filter(query)

            # 排序
            if sort_by:
                doctors = doctors.order_by(sort_by)

        # 将医生和表单添加到上下文中
        context['doctors'] = doctors
        context['form'] = form
        patient_id = self.request.session.get('patient_id')
        context['patient'] = Patient.objects.get(id=patient_id)
        return context
class DoctorDetailView(TemplateView):
    template_name = 'user/doctor_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取医生ID
        doctor_id = kwargs.get('pk')
        # 获取医生对象
        doctor = Doctor.objects.get(id=doctor_id)
        # 获取医生的排班信息
        schedules = DoctorSchedule.objects.filter(doctor=doctor).order_by('date', 'start_time')
        # 将医生和排班信息
        context['doctor'] = doctor
        context['schedules'] = schedules
        # 当前患者信息
        patient_id = self.request.session.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        if patient_id:
            context['patient'] = patient
        # 患者已预约的排班
        user_appointment = Appointment.objects.filter(patient=patient).exclude(status__in=['cancelled', 'completed']).first()
        context['user_appointment'] = user_appointment
        print(user_appointment)
        return context

def book_appointment(request, pk):
    schedule = get_object_or_404(DoctorSchedule, id=pk)

    patient_id = request.session.get('patient_id')
    patient = Patient.objects.get(id=patient_id)

    # 检查用户是否已经预约了该排班
    existing_appointment = Appointment.objects.filter(patient=patient).exclude(status__in=['cancelled', 'completed']).exists()
    if existing_appointment:
        # messages.warning(request, CUSTOM_MESSAGE_LEVEL, '您已经预约了该时间段，不可重复预约。')
        messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '已存在预约时间段，不可重复预约。')
        return redirect('doctor_detail', pk=schedule.doctor.id)

    # 检查排班是否还可预约
    if not schedule.avaliable():
        messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '该时间段已满，无法预约。')
        # messages.warning(request, CUSTOM_MESSAGE_LEVEL, '该时间段已满，无法预约。')
        return redirect('doctor_detail', pk=schedule.doctor.id)

    # 创建新的预约记录
    Appointment.objects.create(
        patient=patient,
        doctor_schedule=schedule,
        status='pending'
    )
    schedule.book()

    # messages.success(request, CUSTOM_MESSAGE_LEVEL, '预约成功，等待医生确认。')
    messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '预约成功，等待医生确认。')

    # 打印消息，调试用
    if messages.get_messages(request):
        print(list(messages.get_messages(request)))
    else:
        print('No messages')
    return redirect('doctor_detail', pk=schedule.doctor.id)

def cancel_appointment(request, pk):
    # patient_id = request.session.get('patient_id')
    # patient = Patient.objects.get(id=patient_id)
    # appointment = get_object_or_404(Appointment, id=pk, patient=patient)
    appointment = get_object_or_404(Appointment, id=pk)
    
    if appointment.status == 'pending' or appointment.status == 'confirmed':
        appointment.cancel()
        messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '预约已取消')
    else:
        messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '无法取消该预约')
    patient_id = request.session.get('patient_id')
    doctor_id = request.session.get('doctor_id')
    if patient_id:
        return redirect('appointment_record')
    elif doctor_id:
        return redirect('check_appointment')
    # return redirect('appointment_record')

class AppointmentRecordView(ListView):
    model = Appointment
    template_name = 'user/appointment_record.html'  # 模板路径
    context_object_name = 'appointments'  # 上下文变量名
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        patient_id = self.request.session.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        context['patient'] = patient
        return context
        
    def get_queryset(self):
        # 获取当前登录用户的预约记录
        patient_id = self.request.session.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        return Appointment.objects.filter(patient=patient).order_by('-created_at')

class ScheduleListView(TemplateView):
    template_name = 'user/schedule_list.html'  # 模板路径
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 获取登录用户
        patient_id = self.request.session.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        context['patient'] = patient

        # 初始化表单
        form = ScheduleFilterForm(self.request.GET or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            gender = form.cleaned_data.get('gender')
            title = form.cleaned_data.get('title')
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            # print("name: ", name)
            # print("gender: ", gender)
            # print("title: ", title)
            # print("date: ", date)
            # print("time: ", time)

            # 根据表单数据过滤医生
            query = Q()
            if name:
                query &= Q(doctor__name__icontains=name)
            if gender:
                query &= Q(doctor__gender=gender)
            if title:
                query &= Q(doctor__title__icontains=title)
            if date:
                query &= Q(date=date)
            if time:
                query &= Q(start_time__lte=time) & Q(end_time__gte=time)

            query &= Q(is_available=True)
                       
            schedules = DoctorSchedule.objects.filter(query)
            context['schedules'] = schedules
            context['form'] = form
        else:
            query = Q()
            query &= Q(is_available=True)
            schedules = DoctorSchedule.objects.filter(query)
            context['schedules'] = schedules
            context['form'] = form
        return context


class PatientMedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'user/patient_medical_records.html'
    context_object_name = 'medical_records'
    paginate_by = 10

    def get_queryset(self):
        patient_id = self.request.session.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        queryset = super().get_queryset().filter(
            appointment__patient=patient
        ).select_related(
            'appointment__doctor_schedule__doctor',
            'appointment__patient'
        )

        # 获取筛选参数
        search_query = self.request.GET.get('search', '')
        doctor_name = self.request.GET.get('doctor_name', '')
        doctor_gender = self.request.GET.get('doctor_gender', '')
        year = self.request.GET.get('year', '')
        month = self.request.GET.get('month', '')
        day = self.request.GET.get('day', '')
        sort_by = self.request.GET.get('sort_by', '-created_at')

        # 构建查询条件
        conditions = Q()
        if search_query:
            conditions |= Q(diagnosis__icontains=search_query)
            conditions |= Q(treatment__icontains=search_query)
            conditions |= Q(appointment__doctor_schedule__doctor__name__icontains=search_query)
        
        if doctor_name:
            conditions &= Q(appointment__doctor_schedule__doctor__name__icontains=doctor_name)

        if doctor_gender:
            conditions &= Q(appointment__doctor_schedule__doctor__gender=doctor_gender)

        # 日期筛选
        date_conditions = Q()
        if year:
            date_conditions &= Q(created_at__year=year)
        if month:
            date_conditions &= Q(created_at__month=month)
        if day:
            date_conditions &= Q(created_at__day=day)
        
        if conditions or date_conditions:
            queryset = queryset.filter(conditions & date_conditions)

        # 处理排序
        valid_sort_fields = {
            '-created_at': '-created_at',
            'created_at': 'created_at',
            'doctor_name': 'appointment__doctor_schedule__doctor__name',
            '-doctor_name': '-appointment__doctor_schedule__doctor__name'
        }
        return queryset.order_by(valid_sort_fields.get(sort_by, '-created_at'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = datetime.now().date()
        
        # 生成筛选选项
        context.update({
            'years': range(current_date.year, current_date.year - 5, -1),
            'months': range(1, 13),
            'days': range(1, 32),
            'search_query': self.request.GET.get('search', ''),
            'doctor_name': self.request.GET.get('doctor_name', ''),
            'selected_year': self.request.GET.get('year', ''),
            'selected_month': self.request.GET.get('month', ''),
            'selected_day': self.request.GET.get('day', ''),
            'sort_by': self.request.GET.get('sort_by', '-created_at')
        })
        return context

class PatientMedicalRecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'user/patient_medical_record_detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        patient_id = self.request.session.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        return super().get_queryset().filter(
            appointment__patient=patient
        ).select_related(
            'appointment__doctor_schedule__doctor',
            'appointment__patient'
        )        

#############################################################################################
######################################### DOCTOR ############################################
#############################################################################################

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

class CheckAppointmentView(LoginRequiredMixin, TemplateView):
    template_name = 'doctor/doctor_check_appointment.html'

    def get(self, request, *args, **kwargs):
        doctor_id = request.session.get('doctor_id')
        doctor = Doctor.objects.get(id=doctor_id)
        # 创建表单实例
        # form = DoctorScheduleForm()
        appointments = Appointment.objects.filter(status__in=['pending', 'confirmed'], doctor_schedule__doctor = doctor).order_by('doctor_schedule__date', 'doctor_schedule__start_time')

        return render(request, self.template_name, {
            'appointments': appointments,
            'doctor': doctor,
        })
    
def confirm_appointment(request, pk):
    
    # doctor_id = request.session.get('doctor_id')
    # doctor = Doctor.objects.get(id=doctor_id)
    appointment = get_object_or_404(Appointment, id=pk)
    
    if appointment.status == 'pending':
        appointment.confirm()
        messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '预约已确认')
    else:
        messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '无法确认该预约')
    
    return redirect('check_appointment')

class ConsultationView(LoginRequiredMixin, TemplateView):
    template_name = 'doctor/consultation.html'  # 模板可以继承 doctor/doctor_home.html

    def get(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, id=kwargs['appointment_id'])
        form = MedicalRecordForm()
        context = {
            'appointment': appointment,
            'form': form,
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        appointment = get_object_or_404(Appointment, id=kwargs['appointment_id'])
        action = request.POST.get('action')
        # 注意：这里构造表单时包含 request.FILES
        form = MedicalRecordForm(request.POST, request.FILES)
        doctor_id = request.session.get('doctor_id')
        doctor = Doctor.objects.get(id=doctor_id)
        # 尝试从隐藏字段中获取之前计算的 AI 建议
        ai_diagnosis = request.POST.get('ai_diagnosis', '')
        top_predictions = None
        if action == 'save':
            if form.is_valid():
                record = form.save(commit=False)
                record.appointment = appointment
                record.ai_diagnosis = ai_diagnosis
                record.save()
                appointment.complete()
                # 保存成功后可跳转到记录详情或其他页面
                return redirect('medical_record_detail', record_id=record.pk)
            else:
                context = {
                    'appointment': appointment,
                    'form': form,
                    'ai_diagnosis': ai_diagnosis,
                    'top_predictions': top_predictions,
                }
                return self.render_to_response(context)
        else:
            # 如果没有特定 action，则返回原页面
            context = {'appointment': appointment, 'form': form, 'doctor': doctor}
            return self.render_to_response(context)

@csrf_exempt  # 如果使用 AJAX，请确保正确处理 CSRF（建议使用 AJAX 时传递 CSRF token）
def upload_image(request):
    if request.method == 'POST':
        upload_file = request.FILES.get('image')
        if not upload_file:
            return JsonResponse({'error': '未上传图片'}, status=400)
        
        # 保存文件到 MEDIA_ROOT，可生成唯一文件名避免冲突
        file_name = upload_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb') as f:
            for chunk in upload_file.chunks():
                f.write(chunk)
        
        try:
            # 加载模型并处理图像（这里参考你的模型代码）
            model = models.mobilenet_v2(pretrained=False)
            num_classes = 7
            model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, num_classes)
            model.load_state_dict(torch.load('model/mobilenetv2_model.pth', map_location=torch.device('cpu')))
            model.eval()

            preprocess = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            image = Image.open(file_path)
            input_tensor = preprocess(image)
            input_batch = input_tensor.unsqueeze(0)
            device = torch.device("cpu")
            model.to(device)
            input_batch = input_batch.to(device)

            with torch.no_grad():
                output = model(input_batch)
            probabilities = F.softmax(output, dim=1)[0]
            top_probabilities, top_indices = torch.topk(probabilities, 3)
            class_names = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

            top_predictions = []
            for i in range(3):
                class_name = class_names[top_indices[i].item()]
                probability = top_probabilities[i].item() * 100
                top_predictions.append({
                    'class_name': class_name,
                    'probability': round(probability, 2)
                })

            # 取最高概率的结果作为 AI 诊断建议
            ai_diagnosis = top_predictions[0]['class_name']

            # 返回 JSON 数据：包含预测结果、AI建议及图片引用（这里直接返回文件路径）
            return JsonResponse({
                'ai_diagnosis': ai_diagnosis,
                'top_predictions': top_predictions,
                'image_url': file_name  # 或者生成一个完整 URL
            })
        except Exception as e:
            return JsonResponse({'error': f'图像处理错误：{str(e)}'}, status=500)
    return JsonResponse({'error': '仅支持 POST 请求'}, status=405)

class MedicalRecordDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'doctor/medical_record_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 获取诊疗记录
        record_id = kwargs.get('record_id') or self.request.GET.get('record_id')
        record = get_object_or_404(
            MedicalRecord.objects.select_related(
                'appointment__patient',
                'appointment__doctor_schedule__doctor'
            ),
            id=record_id,
            appointment__doctor_schedule__doctor_id=self.request.session.get('doctor_id')
        )
        
        # 获取当前医生信息
        doctor_id = self.request.session.get('doctor_id')
        doctor = Doctor.objects.get(id=doctor_id)
        
        context['doctor'] = doctor
        context['record'] = record
        
        return context

class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'doctor/doctor_medical_records.html'
    context_object_name = 'medical_records'
    paginate_by = 10  # 每页显示10条记录

    def get_queryset(self):
        doctor_id = self.request.session.get('doctor_id')
        queryset = super().get_queryset().filter(
            appointment__doctor_schedule__doctor_id=doctor_id
        ).select_related(
            'appointment__patient',
            'appointment__doctor_schedule__doctor'
        ).order_by('-created_at')

        # 搜索和筛选处理
        search_query = self.request.GET.get('search', '')
        patient_name = self.request.GET.get('patient_name', '')
        patient_mobile = self.request.GET.get('patient_mobile', '')
        patient_idcard = self.request.GET.get('patient_idcard', '')
        year = self.request.GET.get('year', '')
        month = self.request.GET.get('month', '')
        day = self.request.GET.get('day', '')
        sort_by = self.request.GET.get('sort_by', '-created_at')

        # 构建查询条件
        conditions = Q()
        if search_query:
            conditions |= Q(appointment__patient__name__icontains=search_query)
            conditions |= Q(appointment__patient__mobile__icontains=search_query)
            conditions |= Q(appointment__patient__idcard__icontains=search_query)
            conditions |= Q(diagnosis__icontains=search_query)
        
        if patient_name:
            conditions &= Q(appointment__patient__name__icontains=patient_name)
        if patient_mobile:
            conditions &= Q(appointment__patient__mobile__icontains=patient_mobile)
        if patient_idcard:
            conditions &= Q(appointment__patient__idcard__icontains=patient_idcard)
        
        # 日期筛选
        date_conditions = Q()
        if year:
            date_conditions &= Q(created_at__year=year)
        if month:
            date_conditions &= Q(created_at__month=month)
        if day:
            date_conditions &= Q(created_at__day=day)
        
        if conditions or date_conditions:
            queryset = queryset.filter(conditions & date_conditions)

        # 排序
        if sort_by in ['created_at', '-created_at', 'appointment__patient__name', '-appointment__patient__name']:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 获取当前年份、月份和日期，用于筛选表单的默认值
        # current_date = datetime.now()
        current_date  = datetime.today().date()
        context['current_year'] = current_date.year
        context['current_month'] = current_date.month
        context['current_day'] = current_date.day
        
        # 获取筛选参数，用于保持表单状态
        context['search_query'] = self.request.GET.get('search', '')
        context['patient_name'] = self.request.GET.get('patient_name', '')
        context['patient_mobile'] = self.request.GET.get('patient_mobile', '')
        context['patient_idcard'] = self.request.GET.get('patient_idcard', '')
        context['selected_year'] = self.request.GET.get('year', '')
        context['selected_month'] = self.request.GET.get('month', '')
        context['selected_day'] = self.request.GET.get('day', '')
        context['sort_by'] = self.request.GET.get('sort_by', '-created_at')
        
        # 生成年份选择列表（最近5年）
        context['years'] = range(current_date.year, current_date.year - 5, -1)
        context['months'] = range(1, 13)
        context['days'] = range(1, 32)

        doctor_id = self.request.session.get('doctor_id')
        doctor = Doctor.objects.get(id=doctor_id)
        context['doctor'] = doctor
        
        return context
