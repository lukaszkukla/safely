from multiprocessing import context
from django.http import Http404
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Hazard


class CustomLoginView(LoginView):
    template_name = 'hazard/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self): 
        return reverse_lazy('hazards')

class HazardList(LoginRequiredMixin, ListView):
    model = Hazard
    context_object_name = 'hazards'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hazards'] = context['hazards'].filter(user=self.request.user)
        context['count'] = context['hazards'].filter(status='1').count()
        return context

class HazardDetail(LoginRequiredMixin, DetailView):
    model = Hazard
    context_object_name = 'hazard'
    template_name = 'hazard/hazard.html'

    def get_object(self, queryset=None):
        hazard = super(DetailView, self).get_object(queryset)
        if hazard.user != self.request.user:
            raise Http404(('Permission Denied'))
        return hazard

class HazardCreate(LoginRequiredMixin, CreateView):
    model = Hazard
    fields = [
        'category',
        'title',
        'slug',
        'image',
        'description',
        'level',
        'status'
    ]    
    success_url = reverse_lazy('hazards')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(HazardCreate, self).form_valid(form)

class HazardUpdate(LoginRequiredMixin, UpdateView):
    model = Hazard
    fields = [
        'category',
        'title',
        'slug',
        'image',
        'description',
        'level',
        'status'
    ]
    success_url = reverse_lazy('hazards')

class HazardDelete(LoginRequiredMixin, DeleteView):
    model = Hazard
    context_object_name = 'hazard'
    success_url = reverse_lazy('hazards')