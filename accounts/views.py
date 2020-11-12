from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core import serializers
from .forms import CustomUserCreationForm
from core.models import Product_List, Category
import csv, json

User=get_user_model()
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'initsignup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        user = form.save()
        login(self.request, user, backend='accounts.backend.EmailBackend')
        return valid


# Create your views here.
