from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout,name='logout'),
    path('create_new_password/',views.create_new_password,name='create_new_password'),
]