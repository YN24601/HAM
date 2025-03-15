from django.db import models
from django.contrib.auth.hashers import make_password  # 用于密码加密
from django.core.validators import RegexValidator
from datetime import datetime, timezone

gender_choices = [
    ('M', '男'),
    ('F', '女'),
]

class Patient(models.Model):
    idcard = models.CharField('身份证号', max_length=20, blank=False, null=False, unique=True)
    name = models.CharField('姓名', max_length=50, blank=False)
    gender = models.CharField('性别', max_length=10, choices=gender_choices)
    mobile = models.CharField('手机号', max_length=11, blank=False, unique=True,
        validators=[RegexValidator(regex='^[0-9]{11}$', message='手机号必须为11位数字')])
    email = models.EmailField('邮箱', max_length=100, unique=True)    
    password = models.CharField('密码', max_length=128)  # 加密后的密码
    # avatar = models.CharField('头像', max_length=100, default='static/images/default_user.jpg')
    avatar = models.ImageField('头像', upload_to='avatars/patients/', default='avatars/patients/default_patient.jpg')
    # avatar = models.CharField('头像', max_length=100, default='/Users/yanazhang/Documents/vscodeProjects/pythonProjects/HAM/DiagnosticSystem/static/images/default_user.jpg')
    created_at = models.DateTimeField('创建时间', auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)

    def set_password(self, raw_password):
        """加密密码并保存"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """检查密码是否匹配"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def getBirthday(self):
        """根据身份证号获取出生日期"""
        if self.idcard and len(self.idcard) >= 14:
            # 身份证号的第7到14位是出生日期
            birthday_str = self.idcard[6:14]
            try:
                # 将字符串转换为日期对象
                birthday = datetime.strptime(birthday_str, "%Y%m%d").date()
                return birthday
            except ValueError:
                # 如果日期格式不正确，返回None
                return None
        return None

    def getAge(self):
        """根据身份证号获取年龄"""
        birthday = self.getBirthday()
        if birthday:
            today = datetime.today().date()
            age = today.year - birthday.year
            # 如果今年生日还没过，年龄减一
            if (today.month, today.day) < (birthday.month, birthday.day):
                age -= 1
            return age
        return None

    def __str__(self):
        return f"{self.name} ({self.idcard})"
    
    class Meta:
        verbose_name = '患者'
        verbose_name_plural = verbose_name

class Doctor(models.Model):
    docID = models.CharField('医生编号', max_length=20, unique=True, null=False, blank=False)
    name = models.CharField('姓名', max_length=50, blank=False)
    title = models.CharField('职称', max_length=50)
    gender = models.CharField('性别', max_length=10, choices=gender_choices)
    birthday = models.DateField('出生日期', null=True, blank=True)
    email = models.EmailField('邮箱', max_length=100, unique=True, blank=False)
    intro = models.TextField('简介', max_length=500, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/doctors/', default='avatars/doctors/default_doctor.jpg')
    password = models.CharField('密码', max_length=128, default='password')
    created_at = models.DateTimeField('创建时间', auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)

    def set_password(self, raw_password):
        """加密密码并保存"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """检查密码是否匹配"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def getBirthday(self):
        # 转为datetime格式
        if self.birthday:
            return datetime.strptime(str(self.birthday), '%Y-%m-%d').date()
        return None

    def getAge(self):
        """根据出生日期获取年龄"""
        if self.birthday:
            today = datetime.today().date()
            age = today.year - self.birthday.year
            # 如果今年生日还没过，年龄减一
            if (today.month, today.day) < (self.birthday.month, self.birthday.day):
                age -= 1
            return age
        return None

    def __str__(self):
        return f"Dr. {self.name} ({self.title})"

    class Meta:
        verbose_name = '医生'
        verbose_name_plural = verbose_name

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='医生')
    date = models.DateField('日期', null=False, blank=False)
    start_time = models.TimeField('开始时间', null=False, blank=False)
    end_time = models.TimeField('结束时间', null=False, blank=False)
    is_available = models.BooleanField('是否可预约', default=True)
    max_patients = models.IntegerField('最大患者数', default=1)
    current_patients = models.IntegerField('当前患者数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time} - {self.end_time}"

    def avaliable(self):
        is_available = self.max_patients > self.current_patients
        return is_available
    
    def book(self):
        self.current_patients += 1
        self.is_available = self.max_patients > self.current_patients
        self.save()

    def cancel(self):
        self.current_patients -= 1
        self.is_available = self.max_patients > self.current_patients
        self.save()

    class Meta:
        verbose_name = '医生排班'
        verbose_name_plural = verbose_name
        unique_together = ('doctor', 'date', 'start_time', 'end_time') # 确保医生在同一日期和时间段内没有重复的排班

class AppointmentStatus(models.TextChoices):
    PENDING = 'pending', '待处理'
    CONFIRMED = 'confirmed', '已确认'
    CANCELLED = 'cancelled', '已取消'
    COMPLETED = 'completed', '已完成'

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='患者')
    doctor_schedule = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE, verbose_name='医生排班')
    status = models.CharField('状态', max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.PENDING)
    notes = models.TextField('备注', max_length=500, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.patient} 预约 {self.doctor_schedule.doctor} - {self.status}"
    
    class Meta:
        verbose_name = '预约记录'
        verbose_name_plural = verbose_name

class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name='预约记录')
    diagnosis = models.TextField('诊断结果', max_length=500, blank=True)
    treatment = models.TextField('治疗方案', max_length=500, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.appointment} - 诊疗结果：{self.diagnosis}"

    class Meta:
        verbose_name = '诊疗记录'
        verbose_name_plural = verbose_name