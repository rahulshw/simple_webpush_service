"""dummy_push_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import index, public_key_view, subscribe_view, push_notif_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('public_key/', public_key_view),
    path('subscribe/', subscribe_view),
    path('trigger_push_notif/', push_notif_view),
    path('dashboard/', dashboard_view)
] + static(settings.ASSETS_URL, document_root=settings.ASSETS_ROOT)
