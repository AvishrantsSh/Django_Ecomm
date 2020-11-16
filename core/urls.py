from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns=[
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/confirm/', TemplateView.as_view(template_name='reg_confirm.html'), name='confirm'),
    path('register/info/', TemplateView.as_view(template_name='seller_info.html'), name='selling_info'),
    path('register/seller/', views.Seller_reg, name='seller_reg'),
    path('sheet/', views.Extract_dt, name='sheet'),
    # path('data/', views.get_dt, name='dt'),
   ]