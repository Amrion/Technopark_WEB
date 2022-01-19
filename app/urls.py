from django.contrib import admin
from django.urls import path

from app import views
from django.conf import settings
from django.conf.urls.static import static

from askme.settings import DEBUG

urlpatterns = [
    path('', views.index, name='home'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:name>', views.tag, name='tag'),
    path('question/<int:number>/', views.question, name='question'),
    path('setting/', views.setting, name='setting'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('ask/', views.ask, name='ask'),
    path('404/', views.error, name='404'),
    path('logout', views.logout, name='logout'),
    path('vote/', views.vote, name='vote'),
    path('correct/', views.correct, name='correct')
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
