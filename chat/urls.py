from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.messages_page,name='messages_page'),
    path('search_users/', views.search_users, name='search_users'),
    path('create_thread/', views.create_thread, name='create_thread'),

]
