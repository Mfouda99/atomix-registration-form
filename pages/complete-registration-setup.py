# settings.py
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'your_app_name',  # Replace with your app name
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'your_project.urls'  # Replace with your project name

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'your_project.wsgi.application'  # Replace with your project name

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files (Uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# models.py
from django.db import models

class Registration(models.Model):
    # Choices for Position dropdown
    POSITION_CHOICES = [
        ('select', 'Select your position'),
        ('LGP', 'LGP'),
        ('LGVP', 'LGVP'),
        ('MM', 'MM'),
        ('TM', 'TM'),
    ]

    # Choices for Function dropdown
    FUNCTION_CHOICES = [
        ('select', 'Select your function'),
        ('OGV', 'OGV'),
        ('OGT', 'OGT'),
        ('ICV', 'ICV'),
        ('IGTa', 'IGTa'),
        ('EDC', 'EDC'),
        ('B2B', 'B2B'),
        ('MCP', 'MCP'),
        ('F&L', 'F&L'),
    ]

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, default='select')
    function = models.CharField(max_length=100, choices=FUNCTION_CHOICES, default='select')
    id_front = models.FileField(upload_to='uploads/')
    id_back = models.FileField(upload_to='uploads/')
    indemnity_form = models.FileField(upload_to='uploads/')
    personal_photo = models.ImageField(upload_to='uploads/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

# forms.py
from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'full_name',
            'phone_number',
            'email_address',
            'position',
            'function',
            'id_front',
            'id_back',
            'indemnity_form',
            'personal_photo'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'email_address': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'position': forms.Select(attrs={
                'class': 'form-control'
            }),
            'function': forms.Select(attrs={
                'class': 'form-control'
            }),
            'id_front': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'id_back': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'indemnity_form': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'personal_photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        position = cleaned_data.get('position')
        function = cleaned_data.get('function')

        if position == 'select':
            raise forms.ValidationError('Please select a valid position')
        if function == 'select':
            raise forms.ValidationError('Please select a valid function')

        return cleaned_data

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from . import RegistrationForm

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('registration')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration.html', {'form': form})

# urls.py (project level)
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('your_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urls.py (app level)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.registration_view, name='registration'),
]
