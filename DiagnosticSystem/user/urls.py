from django.urls import path
from . import views
# from ...DiagnosticSystem.

urlpatterns = [
    path('login/', views.PatientLoginView, name='user_login'),
    path('register/', views.PatientCreateView.as_view(), name='patient_create'),
]