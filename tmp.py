from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core import serializers
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from core.models import Product_List, Category
import csv, json

User=get_user_model()
# class SignUp(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('home')
#     template_name = 'initsignup.html'

#     def form_valid(self, form):
#         valid = super(SignUp, self).form_valid(form)
#         user = form.save()
#         login(self.request, user, backend='accounts.backend.EmailBackend')
#         return valid
def Register(request):
    form = CustomUserCreationForm()
    f_login = CustomAuthenticationForm()
    return render(request,'initsignup.html', {'form':form,'f_login':f_login})

def SignUp(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='accounts.backend.EmailBackend')
            return redirect('home')
                      
    else:
        form = CustomUserCreationForm()
        return redirect('home')

def Login(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user, backend='accounts.backend.EmailBackend')
                return redirect('home')
            else:
                return HttpResponse("You're account is disabled.")
        else:
            return redirect('home')
               
    else:
        return redirect('home')

def Logout(request):
    logout(request)
    return redirect('home')
# Create your views here.
