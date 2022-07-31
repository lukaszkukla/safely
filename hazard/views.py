from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Hazard


class HazardList(ListView):
    model = Hazard
    context_object_name = 'hazards'

class HazardDetail(DetailView):
    model = Hazard
    context_object_name = 'hazard'
    template_name = 'hazard/hazard.html'

class HazardCreate(CreateView):
    model = Hazard
    fields = '__all__'
    success_url = reverse_lazy('hazards')
