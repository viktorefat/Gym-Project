from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Потврди Лозинка")

    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Лозинките не се совпаѓаат!")
        return cleaned_data

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white outline-none focus:border-orange-500 profile-field', 'disabled': 'disabled'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white outline-none focus:border-orange-500 profile-field', 'disabled': 'disabled'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white outline-none focus:border-orange-500 profile-field', 'disabled': 'disabled'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white outline-none focus:border-orange-500 profile-field', 'disabled': 'disabled'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'text-sm text-gray-400 file:mr-4 file:py-1 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-orange-500 file:text-white hover:file:bg-orange-600 profile-field', 'disabled': 'disabled'}))

    class Meta:
        model = Profile
        fields = ['phone', 'avatar']