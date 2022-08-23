from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import is_valid_path, reverse, reverse_lazy
from django.http import Http404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Hazard, Category, Risk, Status
from django.contrib.auth.views import redirect_to_login
from .forms import PasswordChangingForm, LoginForm, UserRegistrationForm, ProfileForm, HazardDetailsForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.forms import UserModel

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class HomePage(TemplateView):
    template_name = 'hazard/pages/index.html'

class PrivacyPolicy(TemplateView):
    template_name = 'hazard/pages/privacy.html'

class CustomLoginView(LoginView):    
    page_title = 'Login'
    context = {}
    form_class = LoginForm

    template_name = 'hazard/pages/auth.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'login'
        context['title'] = 'Login'
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
        context['title'] = 'Register'
        return context


class HazardList(LoginRequiredMixin, ListView):
    model = Hazard
    template_name = 'hazard/pages/hazard.html'
    context_object_name = 'hazards'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'hazard-view'
        context['title'] = 'Hazard Records List View'

        if self.request.user.is_superuser:
            context['unresolved'] = context['hazards'].filter(
                user=self.request.user).exclude(status='3').count()
            context['resolved'] = context['hazards'].filter(
                user=self.request.user, status='3').count()
            context['hazards'] = context['hazards']
        else:
            context['unresolved'] = context['hazards'].filter(
                user=self.request.user).exclude(status='3').count()
            context['resolved'] = context['hazards'].filter(
                user=self.request.user, status='3').count()
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
        context['title'] = 'Hazard Details'
        return context


class HazardCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Class that allows admin to create a new hazard record
    """

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
    success_message = "New hazard created"
    permission_required = 'hazards.view_categories'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(HazardCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'hazard-create'
        context['title'] = 'Hazard Add New'
        return context

    def get_success_url(self):
        return reverse_lazy('hazard', args={self.object.id})


class HazardUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Class that allows logged user to update own hazard record
    """
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
    success_message = "Hazard record updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'hazard-update'
        context['title'] = 'Hazard Update'
        return context

    def get_success_url(self):
        return reverse_lazy('hazard', args={self.object.id})


class HazardDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Class that allows admin to delete own hazard record
    """

    model = Hazard
    template_name = 'hazard/pages/hazard.html'
    context_object_name = 'hazard'
    success_url = reverse_lazy('hazards')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'hazard-delete'
        context['title'] = 'Hazard Delete'
        return context
        

def profileView(request):
    context = {'page': 'profile-view'}
    if request.user.is_authenticated:
        return render(request, 'hazard/components/profile/profile_view.html', context)
    return redirect('login')


def profileEdit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)

            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated")
                return redirect('profile-view')
        else:
            form = EditProfileForm(instance=request.user)
            args = {'form': form}

        return render(request, 'hazard/components/profile/profile_update.html', args)

    return redirect('login')


class UserListView(LoginRequiredMixin, DetailView):
    """
    Class allows to view details of logged user
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
    Class allows to edit details of logged user
    """

    model = User
    form_class = ProfileForm
    template_name = 'hazard/pages/profile.html'
    success_message = "User details updated"
    slug_field = "username"
    raise_exception = False
    permission_required = 'categories.view_categories'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    def get_queryset(self):
        base_qs = super(ProfileUpdateView, self).get_queryset()
        return base_qs.filter(username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'profile-update'
        context['title'] = 'User Profile Update'
        return context

    def get_success_url(self):
        return reverse_lazy('profile-view', args={self.request.user.id})


class EditProfileForm(SuccessMessageMixin, UserChangeForm):
    """
    Form for logged user profile edit
    """

    class Meta:
        """
        Meta class for EditProfileForm
        """
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class PasswordsChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    Class that allows logged user to update own password
    """
    form_class = PasswordChangingForm
    template_name = 'hazard/pages/password.html'
    form_class = PasswordChangeForm
    success_message = "Password updated"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'password-update'
        context['title'] = 'Password Change'
        return context

    def get_success_url(self):
        return reverse_lazy('profile-view', args={self.request.user.id})


class PasswordChangeSuccess(SuccessMessageMixin, PasswordChangeView):
    """
    Class that inform user if the password updated successfully
    """
    form_class = PasswordChangingForm
    template_name = 'hazard/pages/password.html'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'profile-view'
        return context

    def get_success_url(self):
        return reverse_lazy('profile-view', args={self.request.user.id})


class AdminAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/')
        return super(AdminAccessMixin, self).dispatch(request, *args, **kwargs)


class CategoryList(LoginRequiredMixin, AdminAccessMixin, ListView):
    """
    Class that allows admin to view category list
    """

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
        context['title'] = 'Category View'
        return context


class CategoryUpdate(LoginRequiredMixin, AdminAccessMixin,
                     SuccessMessageMixin, UpdateView):
    """
    Class that allows admin to update category item
    """

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
        context['title'] = 'Category Update'
        return context


class CategoryCreate(LoginRequiredMixin, AdminAccessMixin,
                     SuccessMessageMixin, CreateView):
    """
    Class that allows admin to create new category item
    """

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
        context['title'] = 'Category Add New'
        return context


class CategoryDelete(LoginRequiredMixin, AdminAccessMixin,
                     SuccessMessageMixin, DeleteView):
    """
    Class that allows admin to delete category item
    """

    raise_exception = False
    permission_required = 'categories.delete_categories'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Category
    template_name = 'hazard/pages/category.html'
    success_url = reverse_lazy('categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'category-delete'
        context['title'] = 'Category Delete'
        return context


class RiskList(LoginRequiredMixin, AdminAccessMixin, ListView):
    """
    Class that allows admin to view list of risk types
    """

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
        context['title'] = 'Risk View'
        return context


class RiskUpdate(LoginRequiredMixin, AdminAccessMixin,
                 SuccessMessageMixin, UpdateView):
    """
    Class that allows admin to update riks details
    """

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
        context['title'] = 'Risk Update'
        return context


class RiskCreate(LoginRequiredMixin, AdminAccessMixin,
                 SuccessMessageMixin, CreateView):
    """
    Class that allows admin to create a new risk item
    """

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
        context['title'] = 'Risk Add New'
        return context


class RiskDelete(LoginRequiredMixin, AdminAccessMixin,
                 SuccessMessageMixin, DeleteView):
    """
    Class that allows admin to delete risk item
    """

    raise_exception = False
    permission_required = 'risks.delete_risks'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Risk
    template_name = 'hazard/pages/risk.html'
    success_url = reverse_lazy('risks')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'risk-delete'
        context['title'] = 'Risk Delete'
        return context


class StatusList(LoginRequiredMixin, AdminAccessMixin, ListView):
    """
    Class that allows admin to view status list
    """

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
        context['title'] = 'Status List View'
        return context


class StatusUpdate(LoginRequiredMixin, AdminAccessMixin,
                   SuccessMessageMixin, UpdateView):
    """
    Class that allows admin to update status item
    """

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
        context['title'] = 'Status Update'
        return context


class StatusCreate(LoginRequiredMixin, AdminAccessMixin,
                   SuccessMessageMixin, CreateView):
    """
    Class that allows admin to create a new status item
    """

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
        context['title'] = 'Status Add New'
        return context


class StatusDelete(LoginRequiredMixin, AdminAccessMixin,
                   SuccessMessageMixin, DeleteView):
    """
    Class that allows admin to delete status item
    """

    raise_exception = False
    permission_required = 'statuses.delete_statuses'
    permission_denied_message = ""
    login_url = 'hazards'
    redirect_field_name = 'next'

    model = Status
    template_name = 'hazard/pages/status.html'
    success_url = reverse_lazy('statuses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'status-delete'
        context['title'] = 'Status Delete'
        return context


def error404View(request, exception=None):
    """ A view to return the 404 page """

    return render(request, 'hazard/pages/404.html')


def server_error_500(request):
    """ A view to return the 500 page """

    return render(request, 'hazard/pages/500.html')
