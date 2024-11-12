from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages




def home(request):
   return render(request, 'home.html', {'name': 'fouda'})







