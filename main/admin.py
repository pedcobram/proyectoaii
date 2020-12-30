from django.contrib import admin
from main.models import Anime, Genero, InformacionUsuario, Calificacion

# Register your models here.

admin.site.register(Anime)
admin.site.register(Genero)
admin.site.register(InformacionUsuario)
admin.site.register(Calificacion)