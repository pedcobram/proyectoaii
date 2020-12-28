#encoding:utf-8
from django.db import models

class Genero(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Género')

    def __str__(self):
        return self.nombre

class Anime(models.Model):
    titulo = models.TextField(verbose_name='Título')
    imagen = models.TextField(verbose_name='URL de imagen')
    rango = models.TextField(verbose_name='Rango de la web')
    popularidad = models.TextField(verbose_name='Popularidad de la web')
    episodios = models.TextField(verbose_name='Número de episodios');
    sinopsis = models.TextField(verbose_name='Sinopsis', null=True);
    fechaInicio = models.DateField(verbose_name='Fecha de Inicio', null=True)
    fechaFinal = models.DateField(verbose_name='Fecha de Final', null=True)
    generos = models.ManyToManyField(Genero)

    def __str__(self):
        return self.titulo
    

