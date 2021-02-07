"""QuonoidTask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from Task1.views import *
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',CreateAccount.as_view(),name="CreateAccount"),
    path('',lambda x:redirect("CreateAccount"),name="redirectTo"),
    path("login",Login.as_view(),name="Login"),
    path("logout",Logout.as_view(),name="logout"),
    path("home",UserHome.as_view(),name="Home"),
    path("activities",Loadactivities.as_view(),name="Loadactivities"),
    path("fetch/more",FetchmoreActivites.as_view(),name="FetchmoreActivites"),
    path("update",UpdateActivites.as_view(),name="UpdateActivites"),
    path("delete",DeleteActivity.as_view(),name="DeleteActivity"),
]
