from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
User=get_user_model()
LOCK_URLS = (
            "/register/seller/",
             )
LOGIN_URL = ("/accounts/register/")
LOGOUT_URL = ("/accounts/logout/")

class AuthRequired(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        assert hasattr(request, 'user')
        path = request.path_info
        
        if not request.user.is_authenticated and str(path) in LOCK_URLS:
            return HttpResponseRedirect(reverse('login')+'?next='+request.path) # or http response
            
        