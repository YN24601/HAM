from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from .mixins import LoginRequiredMixin

class HomeView(TemplateView):
    template_name = 'home.html'
    
class DiseaseView(LoginRequiredMixin, TemplateView):
    template_name = 'disease_intro.html'
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return JsonResponse({'status': 'authenticated'})
        return super().get(request, *args, **kwargs)


