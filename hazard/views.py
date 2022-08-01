from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from .models import Hazard


class CustomLoginView(LoginView):
    template_name = 'hazard/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self): 
        return reverse_lazy('hazards')


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

class HazardUpdate(UpdateView):
    model = Hazard
    fields = '__all__'
    success_url = reverse_lazy('hazards')

class HazardDelete(DeleteView):
    model = Hazard
    context_object_name = 'hazard'
    success_url = reverse_lazy('hazards')