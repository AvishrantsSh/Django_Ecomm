from django.urls import path
from .import views

urlpatterns=[
    # path('register/',views.Register,name='reg'),
    path('register/', views.SignUp, name='reg'),
    # path('login/',views.Login,name='login'),
    path('logout/', views.Logout, name='logout'),
   ]