"""mysites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from show import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('register/',views.register),
    path('signin/',views.signin),
    path('signup/',views.signup),
    path('index/',views.index),
    path('search/',views.search),
    path('addTask/',views.addTask),
    path('add/',views.add),
    url(r'^show/$',views.show),
    url(r'^detail/$',views.detail),
    url(r'^analyze/$',views.analyze),
    url(r'^delete/$',views.delete),
    url(r'^download/$', views.export_users_xls, name='export_users_xls'),
    path('info/',views.info),
    path('loginout/',views.loginout),
    path('alterinfo/',views.alterinfo),
]
