# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate
from .models import User

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user or not user.is_active:
                raise forms.ValidationError('Invalid credentials. Please try again.')

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}))

    class Meta:
        model = User
        fields = ('name','email', 'password1', 'password2')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}),
            'password1': forms.PasswordInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}),
            'password2': forms.PasswordInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}),
        }

class ForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}))

class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}))
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput(attrs={'class': 'input py-2 px-3 w-full border rounded-lg shadow-sm focus:outline-none focus:border-blue-500'}))
