from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns=[
    path('', TemplateView.as_view(template_name='about.html'), name='about'),
    path('home/', views.HomeView, name='home'),
    path('profile/', views.Profile, name='profile'),
    path('register/confirm/', TemplateView.as_view(template_name='reg_confirm.html'), name='confirm'),
    path('register/info/', TemplateView.as_view(template_name='seller_info.html'), name='selling_info'),
    path('register/seller/', views.Seller_reg, name='seller_reg'),
    path('sheet/', views.Extract_dt, name='sheet'),
    path('search/', views.Products, name='search'),
    path('shop/<cat>/<store>/<pk>/', views.Seller_Landing, name='seller_shop'),
    path('product/<pk>', views.Product_Dscr, name='product'),
    # path('data/', views.get_dt, name='dt'),
   ]