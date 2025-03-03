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
    path('doctor_intro/', views.DoctorIntroView.as_view(), name="doctor_intro"),
    # path('doctor_intro/<int:pk>/', views.DoctorDetailView.as_view(), name="doctor_detail"),

    path("profile/", views.PatientProfileView.as_view(), name="profile"),

    path('doctor_login/', views.DoctorLoginView.as_view(), name='doctor_login'),
    path('doctor_home/', views.DoctorHomeView.as_view(), name='doctor_home'),
    path('doctor_logout/', views.DoctorLogout, name='doctor_logout'),
]