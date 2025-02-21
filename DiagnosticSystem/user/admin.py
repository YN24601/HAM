from django.contrib import admin
from django.contrib.auth.hashers import make_password
# Register your models here.
from .models import Patient, Doctor, DoctorSchedule, Appointment, MedicalRecord

class DoctorAdmin(admin.ModelAdmin):
    # 在 admin 界面中显示字段
    list_display = ('docID', 'name', 'title', 'email', )
    # exclude = ('password',)

    # 重写保存方法，确保密码被加密
    def save_model(self, request, obj, form, change):
        if obj.password and not obj.password.startswith('pbkdf2_sha256$'):  # 检查密码是否已加密
            obj.password = make_password(obj.password)  # 加密密码
        super().save_model(request, obj, form, change)

class PatientAdmin(admin.ModelAdmin):
    list_display = ('idcard', 'name', 'gender', 'mobile', 'email')
    exclude = ('password',)


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorSchedule)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)