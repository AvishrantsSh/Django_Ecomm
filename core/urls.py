from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns=[
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/confirm/', TemplateView.as_view(template_name='reg_confirm.html'), name='confirm'),
    path('register/seller/', views.Seller_reg, name='seller_reg'),
   ]