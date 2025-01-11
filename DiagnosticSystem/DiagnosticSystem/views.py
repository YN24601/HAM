from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
    
class LoginView(TemplateView):
    template_name = 'login.html'

class RegisterView(TemplateView):
    template_name = 'register.html'
    # 用户点击登陆按钮 转跳到登陆页面
    def get(self, request):
        return render(request, 'login.html')