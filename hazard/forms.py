from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Hazard


class PasswordChangingForm(PasswordChangeForm):
    """
    Creates form for user to change password
    """
    old_password = forms.CharField(
        max_length=100,
        label='Old Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'col-12 input-main form-control', 'type': 'password'
            }
        )
    )
    new_password1 = forms.CharField(
        max_length=100,
        label='New Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'col-12 input-main form-control', 'type': 'password'
            }
        )
    )
    new_password2 = forms.CharField(
        max_length=100,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'col-12 input-main form-control', 'type': 'password'
            }
        )
    )

    class Meta:
        """
        Meta class for password changing form
        """
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class LoginForm(AuthenticationForm):
    """
    Creates form for user to login
    """
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'col-12 input-main form-control',
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'col-12 input-main form-control',
            }
        )
    )


class UserRegistrationForm(UserCreationForm):
    """
    Creates form for user to register a new account
    """
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'col-12 input-main form-control',
            }
        )
    )
    password1 = forms.CharField(
        max_length=150,
        label='New Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'col-12 input-main form-control', 'type': 'password'
            }
        )
    )
    password2 = forms.CharField(
        max_length=150,
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'col-12 input-main form-control', 'type': 'password'
            }
        )
    )

    class Meta:
        """
        Meta class for user registration form
        """
        model = User
        fields = ('username', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    """
    Creates user profile form
    """
    class Meta:
        """
        Meta class for profile form
        """
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]


class HazardDetailsForm(forms.ModelForm):
    """
    Creates hazard details form
    """
    # category = forms.CharField(
    #     max_length=200,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'col-12 input-main form-control'
    #         }
    #     )
    # )
    # title = forms.CharField(
    #     max_length=200,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'col-12 input-main form-control'
    #         }
    #     )
    # )

    
    class Meta:
        model = Hazard
        fields = '__all__'
