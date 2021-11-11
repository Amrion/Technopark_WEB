from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:name>', views.tag, name='tag'),
    path('question/<int:number>/', views.question, name='question'),
    path('setting/', views.setting, name='setting'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('ask/', views.ask, name='ask'),
    path('404/', views.error, name='404')
]