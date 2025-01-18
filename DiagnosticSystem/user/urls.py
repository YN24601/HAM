from django.urls import path
from . import views
# from ...DiagnosticSystem.

# user/
urlpatterns = [
    path('login/', views.PatientLoginView.as_view(), name='user_login'),
    path('register/', views.PatientCreateView.as_view(), name='patient_create'),
    path('home/', views.PatientHomeView.as_view(), name='dashboard'),
    path('logout/', views.PatientLogout, name='patient_logout'),
]