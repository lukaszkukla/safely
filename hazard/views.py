from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import is_valid_path, reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Hazard, Category, Risk, Status

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


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

class AdminAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/')
        return super(AdminAccessMixin, self).dispatch(request, *args, **kwargs)

class CategoryList(LoginRequiredMixin, AdminAccessMixin, ListView):

    raise_exception = False
    permission_required = 'categories.view_categories'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Category
    context_object_name = 'categories'
    template_name = 'hazard/category_list.html'


class CategoryUpdate(LoginRequiredMixin, AdminAccessMixin, UpdateView):
    
    raise_exception = False
    permission_required = 'categories.change_categories'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Category
    template_name = 'hazard/update_category.html'
    fields = '__all__'
    success_url = reverse_lazy('categories')


class CategoryCreate(LoginRequiredMixin, AdminAccessMixin, CreateView):
    
    raise_exception = False
    permission_required = 'categories.add_categories'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Category
    fields = '__all__'
    success_url = reverse_lazy('categories')


class CategoryDelete(LoginRequiredMixin, AdminAccessMixin, DeleteView):
    
    raise_exception = False
    permission_required = 'categories.delete_categories'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'
    
    model = Category
    success_url = reverse_lazy('categories')


class RiskList(LoginRequiredMixin, AdminAccessMixin, ListView):
    
    raise_exception = False
    permission_required = 'risks.view_risks'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'
    
    model = Risk
    context_object_name = 'risks'
    template_name = 'hazard/risk_list.html'


class RiskUpdate(LoginRequiredMixin, AdminAccessMixin, UpdateView):
    
    raise_exception = False
    permission_required = 'risks.change_risks'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'
    
    model = Risk
    template_name = 'hazard/update_risk.html'
    fields = '__all__'
    success_url = reverse_lazy('risks')


class RiskCreate(LoginRequiredMixin, AdminAccessMixin, CreateView):
    
    raise_exception = False
    permission_required = 'risks.add_risks'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Risk
    fields = '__all__'
    success_url = reverse_lazy('risks')


class RiskDelete(LoginRequiredMixin, AdminAccessMixin, DeleteView):
    
    raise_exception = False
    permission_required = 'risks.delete_risks'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'
    
    model = Risk
    success_url = reverse_lazy('risks')


class StatusList(LoginRequiredMixin, AdminAccessMixin, ListView):
    
    raise_exception = False
    permission_required = 'statuses.view_statuses'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'
    
    model = Status
    context_object_name = 'statuses'
    template_name = 'hazard/status_list.html'


class StatusUpdate(LoginRequiredMixin, AdminAccessMixin, UpdateView):
    
    raise_exception = False
    permission_required = 'statuses.change_statuses'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'
    
    model = Status
    template_name = 'hazard/update_status.html'
    fields = '__all__'
    success_url = reverse_lazy('statuses')


class StatusCreate(LoginRequiredMixin, AdminAccessMixin, CreateView):
    
    raise_exception = False
    permission_required = 'statuses.add_statuses'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'
    
    model = Status
    fields = '__all__'
    success_url = reverse_lazy('statuses')


class StatusDelete(LoginRequiredMixin, AdminAccessMixin, DeleteView):
    
    raise_exception = False
    permission_required = 'statuses.delete_statuses'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Status
    success_url = reverse_lazy('statuses')
