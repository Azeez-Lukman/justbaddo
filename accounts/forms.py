"""
Django forms for user authentication, registration, password recovery, and onboarding.
Provides robust server-side validation, anti-enumeration error handling, and password policy enforcement.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Username or Email",
        max_length=254,
        widget=forms.TextInput(attrs={
            'id': 'jb-login-identifier',
            'autocomplete': 'username',
            'placeholder': 'e.g. baddofan99 or fan@example.com',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl pl-10 pr-3 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none transition-colors'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'id': 'jb-login-password',
            'autocomplete': 'current-password',
            'placeholder': 'Enter your password',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl pl-10 pr-10 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none transition-colors'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'id': 'jb-login-remember',
            'class': 'w-3.5 h-3.5 accent-amber-500 rounded'
        })
    )
    next = forms.CharField(required=False, widget=forms.HiddenInput())

class RegistrationForm(forms.Form):
    display_name = forms.CharField(
        label="Display Name",
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={
            'id': 'jb-reg-name',
            'placeholder': 'e.g. Babatunde Lawal',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl px-3.5 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none transition-colors'
        })
    )
    username = forms.CharField(
        label="Username",
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={
            'id': 'jb-reg-username',
            'autocomplete': 'username',
            'placeholder': 'baddofan99',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl pl-8 pr-3 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none transition-colors'
        })
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'id': 'jb-reg-email',
            'autocomplete': 'email',
            'placeholder': 'you@domain.com',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl px-3.5 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none transition-colors'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'id': 'jb-reg-password',
            'autocomplete': 'new-password',
            'placeholder': 'At least 8 characters (letters & numbers)',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl pl-3.5 pr-10 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none transition-colors'
        })
    )
    terms_accepted = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must accept the Terms of Service and Privacy Policy to create an account.'},
        widget=forms.CheckboxInput(attrs={
            'id': 'jb-reg-terms',
            'class': 'w-4 h-4 mt-0.5 accent-amber-500 rounded cursor-pointer'
        })
    )
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_username(self):
        username = self.cleaned_data['username'].strip().lower()
        if not username.isalnum() and not all(c.isalnum() or c in '_-' for c in username):
            raise ValidationError("Usernames may only contain letters, numbers, underscores, and hyphens.")
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Registered Email Address",
        widget=forms.EmailInput(attrs={
            'id': 'jb-forgot-email',
            'autocomplete': 'email',
            'placeholder': 'you@domain.com',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl pl-10 pr-3.5 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none transition-colors'
        })
    )

class SetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'id': 'jb-new-password',
            'autocomplete': 'new-password',
            'placeholder': 'Enter your new strong password',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl pl-3.5 pr-10 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none transition-colors'
        })
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'id': 'jb-confirm-password',
            'autocomplete': 'new-password',
            'placeholder': 'Confirm your new password',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl pl-3.5 pr-10 py-2.5 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none transition-colors'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "The two password fields did not match.")
        if p1:
            validate_password(p1)
        return cleaned_data

class WelcomePersonalisationForm(forms.Form):
    country = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'jb-pers-country',
            'placeholder': 'e.g. Nigeria, United Kingdom, United States',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl px-3.5 py-2 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none'
        })
    )
    bio = forms.CharField(
        required=False,
        max_length=300,
        widget=forms.Textarea(attrs={
            'id': 'jb-pers-bio',
            'rows': 2,
            'placeholder': 'Tell fellow fans about your love for Baddo music...',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl p-3 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none resize-none'
        })
    )
    favorite_album = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'jb-pers-album',
            'placeholder': 'e.g. Time and Space, Carpe Diem, YBNL',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl px-3.5 py-2 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none'
        })
    )
    favorite_track = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'jb-pers-track',
            'placeholder': 'e.g. Jaiye, Infinity, Wo!!',
            'class': 'w-full bg-zinc-950 border border-zinc-800 focus:border-amber-500 rounded-xl px-3.5 py-2 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none'
        })
    )
