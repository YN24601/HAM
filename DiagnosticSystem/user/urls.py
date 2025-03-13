from django.urls import path
from . import views
# from ...DiagnosticSystem.

# user/
urlpatterns = [
    path('login/', views.PatientLoginView.as_view(), name='user_login'),
    path('register/', views.PatientCreateView.as_view(), name='patient_create'),
    path('home/', views.PatientHomeView.as_view(), name='dashboard'),
    path('logout/', views.PatientLogout, name='patient_logout'),
    path("disease_intro/", views.DiseaseViewForUser.as_view(), name="disease_intro_for_users"),
    path('disease_intro/akiec', views.AKIECView.as_view(), name='akiec'),
    path('disease_intro/bcc', views.BCCView.as_view(), name='bcc'),
    path('disease_intro/bkl', views.BKLView.as_view(), name='bkl'),
    path('disease_intro/df', views.DFView.as_view(), name='df'),
    path('disease_intro/nv', views.NVView.as_view(), name='nv'),
    path('disease_intro/mel', views.MELView.as_view(), name='mel'),
    path('disease_intro/vasc', views.VASCView.as_view(), name='vasc'),
    # path('doctor_intro/', views.DoctorIntroView.as_view(), name="doctor_intro_for_users"),
    # path('doctor_intro/<int:pk>/', views.DoctorDetailView.as_view(), name="doctor_detail"),
    # path('doctors_list/', views.doctor_list, name='doctors_list'),
    path('doctors_list/', views.DoctorListView.as_view(), name='doctors_list'),
    path('doctor_detail/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('book_appointment/<int:pk>/', views.book_appointment, name='book_appointment'),
    path('appointment_record/', views.AppointmentRecordView.as_view(), name='appointment_record'),
    path('cancel_appointment/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
    path('schedule_list/', views.ScheduleListView.as_view(), name='schedule_list'),


    path("profile/", views.PatientProfileView.as_view(), name="profile"),
    path('doctor_login/', views.DoctorLoginView.as_view(), name='doctor_login'),
    path('doctor_home/', views.DoctorHomeView.as_view(), name='doctor_home'),
    path('doctor_logout/', views.DoctorLogout, name='doctor_logout'),
    path('doctor_profile/', views.DoctorProfileView.as_view(), name='doctor_profile'),
    path('doctor_schedule/', views.DoctorScheduleView.as_view(), name='doctor_schedule'),
    path('doctor_schedule/delete/<int:pk>/', views.DoctorScheduleDelete, name='doctor_schedule_delete'),
    path('doctor_schedule/edit/<int:pk>/', views.DoctorScheduleEditView.as_view(), name='doctor_schedule_edit'),

]