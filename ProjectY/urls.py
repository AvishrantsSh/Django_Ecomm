"""ProjectY URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
# from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',include('core.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('manifest.json',TemplateView.as_view(template_name='pwa/manifest.json',content_type='text/plain')),
    path('serviceworker.js',TemplateView.as_view(template_name='pwa/serviceworker.js',content_type='text/javascript')),
    path('error/', TemplateView.as_view(template_name='404.html'), name='404'),
    path('<pth>', TemplateView.as_view(template_name='404.html')),
    # path('media/<path>', serve,{'document_root': settings.MEDIA_ROOT}),
    # path('static/<path>', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
