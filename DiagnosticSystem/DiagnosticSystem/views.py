from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
    
class DiseaseView(TemplateView):
    template_name = 'disease_intro.html'

