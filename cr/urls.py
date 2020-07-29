"""miniprojet URL Configuration

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
from django.urls import path, re_path

from carental import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),

    path('reserve', views.reserve, name="reserve"),
    path('admin/reservations', views.reservations, name="reservations"),
    path('possibe_reservation', views.possibe_reservation, name="possibe_reservation"),

    path('admin/add_car/', views.add_car, name="add_car"),
    path('admin/update_car/', views.update_car, name="update_car"),

    path('cars/', views.cars, name="cars"),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='carental/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='carental/logout.html'), name='logout'),

    path('promotion/', views.promotion, name='promotion'),
    path('penalize/', views.penalize, name='penalize'),
    path('penalties/', views.penalties, name='penalties'),
    path('cancellations/', views.cancellations, name='cancellations'),
    path('add_balance/', views.add_balance, name='add_balance'),

    path('admin/', admin.site.urls),
]
