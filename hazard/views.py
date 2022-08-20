from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import is_valid_path, reverse, reverse_lazy
from django.http import Http404

from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Hazard, Category, Risk, Status

from .forms import PasswordChangingForm, LoginForm, UserRegistrationForm, ProfileForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.forms import UserModel

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class CustomLoginView(LoginView):
    page_title = 'Login'
    context = {}
    form_class = LoginForm

    template_name = 'hazard/pages/auth.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('hazards')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'login'
        return context


class Register(SuccessMessageMixin, FormView):
    page_title = 'Register'
    context = {}
    context['page'] = 'register'
    template_name = 'hazard/pages/auth.html'
    form_class = UserRegistrationForm
    register = True
    redirect_authenticated_user = True
    success_url = reverse_lazy('hazards')
    success_message = "You have registered successfully"

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('hazards')
        return super(Register, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'register'
        return context


class HazardList(LoginRequiredMixin, ListView):
    model = Hazard
    template_name = 'hazard/pages/hazard.html'
    context_object_name = 'hazards'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'hazard-view'
        
        if self.request.user.is_superuser:
            context['unresolved'] = context['hazards'].filter(user=self.request.user).exclude(status='3').count()
            context['resolved'] = context['hazards'].filter(user=self.request.user, status='3').count()
            context['hazards'] = context['hazards']
        else:
            context['unresolved'] = context['hazards'].filter(user=self.request.user).exclude(status='3').count()
            context['resolved'] = context['hazards'].filter(user=self.request.user, status='3').count()
            context['hazards'] = context['hazards'].filter(
                user=self.request.user)

        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['hazards'] = context['hazards'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        return context    


class HazardDetail(LoginRequiredMixin, DetailView):
    model = Hazard
    template_name = 'hazard/pages/hazard.html'
    context_object_name = 'hazard'

    def get_object(self, queryset=None):
        hazard = super(DetailView, self).get_object(queryset)
        if hazard.user == self.request.user or self.request.user.is_staff:
            return hazard
        else:
            raise Http404(('Permission Denied'))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'hazard-detail-view'
        return context    


class HazardCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Hazard
    template_name = 'hazard/pages/hazard.html'
    fields = [
        'category',
        'title',
        'image',
        'description',
        'level',
        'status'
    ]
    success_url = reverse_lazy('hazards')
    success_message = "New hazard created"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(HazardCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'hazard-create'
        return context


class HazardUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Hazard
    template_name = 'hazard/pages/hazard.html'
    fields = [
        'category',
        'title',
        'image',
        'description',
        'level',
        'status'
    ]
    success_url = reverse_lazy('hazards')
    success_message = "Hazard record updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'hazard-update'
        return context


class HazardDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Hazard
    template_name = 'hazard/pages/hazard.html'
    context_object_name = 'hazard'
    success_url = reverse_lazy('hazards')
    success_message = "Hazard record deleted"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'hazard-delete'
        return context


# class ProfileView(DetailView):
#     model = get_user_model()
#     context_object_name = 'user_object'
#     template_name = 'accounts/profile.html'
    

class UserListView(DetailView):
    """
    Class to list all the user
    """
    model = User
    slug_field = 'username'
    template_name = 'hazard/pages/profile.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'profile-view'
        context['title'] = 'User Profile'
        return context

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Class that only allows authentic user to update their profile
    Composed of first_name, last_name
    """
    model = User
    form_class = ProfileForm
    template_name = 'hazard/pages/profile.html'
    success_message = "User details updated"  
    success_url = reverse_lazy('profile-view')
    slug_field = "username"
    redirect_field_name = 'next'

    def get_queryset(self):
        base_qs = super(ProfileUpdateView, self).get_queryset()
        return base_qs.filter(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'profile-update'
        return context


class EditProfileForm(SuccessMessageMixin, UserChangeForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class PasswordsChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'hazard/pages/password.html'
    # form_class = PasswordChangeForm
    success_url = reverse_lazy('profile-view')
    success_message = "Password updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'password-update'
        context['title'] = 'Password Change'
        return context


class PasswordChangeSuccess(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'hazard/pages/password.html'    
    redirect_field_name = 'next'

    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('profile-view', kwargs={'pk': kwargs['idnumber']})
        else:
            return reverse_lazy('profile-view', args=(self.object.id,))

    def user_id(self, object_id):
        user = User.objects.get(id=object_id)
        return self.get_success_url(idnumber=user.id)

    # def get_success_url(self, **kwargs):
    #     return reverse("newJob")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'profile-view'
        return context


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
    template_name = 'hazard/pages/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'category-view'
        return context


class CategoryUpdate(LoginRequiredMixin, AdminAccessMixin, SuccessMessageMixin, UpdateView):

    raise_exception = False
    permission_required = 'categories.change_categories'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Category
    template_name = 'hazard/pages/category.html'
    fields = '__all__'
    success_url = reverse_lazy('categories')
    success_message = "Category updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'category-update'
        return context


class CategoryCreate(LoginRequiredMixin, AdminAccessMixin, SuccessMessageMixin, CreateView):

    raise_exception = False
    permission_required = 'categories.add_categories'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Category
    template_name = 'hazard/pages/category.html'
    fields = '__all__'
    success_url = reverse_lazy('categories')
    success_message = "Category created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'category-create'
        return context    


class CategoryDelete(LoginRequiredMixin, AdminAccessMixin, SuccessMessageMixin, DeleteView):

    raise_exception = False
    permission_required = 'categories.delete_categories'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Category
    template_name = 'hazard/pages/category.html'
    success_url = reverse_lazy('categories')
    success_message = "Category deleted"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'category-delete'
        return context


class RiskList(LoginRequiredMixin, AdminAccessMixin, ListView):

    raise_exception = False
    permission_required = 'risks.view_risks'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Risk
    template_name = 'hazard/pages/risk.html'
    context_object_name = 'risks'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'risk-view'
        return context


class RiskUpdate(LoginRequiredMixin, AdminAccessMixin, SuccessMessageMixin, UpdateView):

    raise_exception = False
    permission_required = 'risks.change_risks'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Risk
    template_name = 'hazard/pages/risk.html'
    fields = '__all__'
    success_url = reverse_lazy('risks')
    success_message = "Risk updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'risk-update'
        return context


class RiskCreate(LoginRequiredMixin, AdminAccessMixin, SuccessMessageMixin, CreateView):

    raise_exception = False
    permission_required = 'risks.add_risks'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Risk
    template_name = 'hazard/pages/risk.html'
    fields = '__all__'
    success_url = reverse_lazy('risks')
    success_message = "Risk created"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'risk-create'
        return context


class RiskDelete(LoginRequiredMixin, AdminAccessMixin, SuccessMessageMixin, DeleteView):

    raise_exception = False
    permission_required = 'risks.delete_risks'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Risk
    template_name = 'hazard/pages/risk.html'
    success_url = reverse_lazy('risks')
    success_message = "Risk deleted"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'risk-delete'
        return context


class StatusList(LoginRequiredMixin, AdminAccessMixin, ListView):

    raise_exception = False
    permission_required = 'statuses.view_statuses'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Status
    template_name = 'hazard/pages/status.html'
    context_object_name = 'statuses'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'status-view'
        return context


class StatusUpdate(LoginRequiredMixin, AdminAccessMixin, SuccessMessageMixin, UpdateView):

    raise_exception = False
    permission_required = 'statuses.change_statuses'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Status
    template_name = 'hazard/pages/status.html'
    fields = '__all__'
    success_url = reverse_lazy('statuses')
    success_message = "Status updated"    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'status-update'
        return context


class StatusCreate(LoginRequiredMixin, AdminAccessMixin, SuccessMessageMixin, CreateView):

    raise_exception = False
    permission_required = 'statuses.add_statuses'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Status
    template_name = 'hazard/pages/status.html'
    fields = '__all__'
    success_url = reverse_lazy('statuses')
    success_message = "Status created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'status-create'
        return context


class StatusDelete(LoginRequiredMixin, AdminAccessMixin, SuccessMessageMixin, DeleteView):

    raise_exception = False
    permission_required = 'statuses.delete_statuses'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Status
    template_name = 'hazard/pages/status.html'
    success_url = reverse_lazy('statuses')
    success_message = "Status deleted"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'status-delete'
        return context


def Error404View(request, exception):
    """ Error Page 404 - Page Not Found """
    return render(request, "404.html")
