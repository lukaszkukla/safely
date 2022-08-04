from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import is_valid_path, reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Hazard, Category

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from django.db import models


class CustomLoginView(LoginView):
    template_name = 'hazard/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self): 
        return reverse_lazy('hazards')

class Register(FormView):
    template_name = 'hazard/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('hazards')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('hazards')
        return super(Register, self).get(*args, **kwargs)

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

def profileView(request):
    args = {'user', request.user}
    if request.user.is_authenticated:
        return render(request, 'hazard/profile.html')
    return redirect('login')
    
def profileEdit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                return redirect('/profile')
        else:
            form = EditProfileForm(instance=request.user)
            args = {'form': form}
            return render(request, 'hazard/edit_profile.html', args)
    return redirect('login')

class EditProfileForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'hazard/category_list.html'

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'hazard/update_category.html'
    fields = '__all__'
    success_url = reverse_lazy('categories')

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'   
    success_url = reverse_lazy('categories')

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('categories')
