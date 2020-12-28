#encoding:utf-8

from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('', views.index), 
    path("carga/", views.carga),
    path("animes/", views.lista_animes),
    path('buscaranimesporfechainicio/', views.buscar_animesporfechainicio),
    path('buscaranimesporgenero/', views.buscar_animesporgenero),
    path('admin/', admin.site.urls),
]
