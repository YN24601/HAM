from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, ListView
from django.db.models import Q
CUSTOM_MESSAGE_LEVEL = 10  # 自定义消息级别
from .models import Patient, Doctor, DoctorSchedule, Appointment, AppointmentStatus
from .forms import PatientCreationForm, PatientLoginForm, PatientForm, DoctorFilterForm, ScheduleFilterForm
from .forms import DoctorLoginForm, DoctorForm, DoctorScheduleForm
from DiagnosticSystem.mixins import LoginRequiredMixin
from datetime import date, timedelta


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

    # messages.success(request, CUSTOM_MESSAGE_LEVEL, '预约成功，等待医生确认。')
    messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '预约成功，等待医生确认。')

    # 打印消息，调试用
    if messages.get_messages(request):
        print(list(messages.get_messages(request)))
    else:
        print('No messages')
    return redirect('doctor_detail', pk=schedule.doctor.id)

def cancel_appointment(request, pk):
    patient_id = request.session.get('patient_id')
    patient = Patient.objects.get(id=patient_id)
    appointment = get_object_or_404(Appointment, id=pk, patient=patient)
    
    if appointment.status == 'pending':
        appointment.status = 'cancelled'
        appointment.save()
        messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '预约已取消')
    else:
        messages.add_message(request, CUSTOM_MESSAGE_LEVEL, '无法取消该预约')
    
    return redirect('appointment_record')

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