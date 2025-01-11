from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.LoginView.as_view(), name='user_login'),
    path('register/', views.UserCreateView.as_view(), name='user_create'),
]