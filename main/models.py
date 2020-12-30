#encoding:utf-8
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

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
    
class InformacionUsuario(models.Model):
    edad = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name='Edad')
    genero = models.CharField(max_length=1, choices=(('F', 'Femenino'),('M','Masculino'),), verbose_name='Genero')
    codigoPostal = models.CharField(max_length=8, verbose_name="Código Postal")
    def __str__(self):
        return self.genero + " " + self.codigoPostal

class Calificacion(models.Model):
    usuario = models.ForeignKey(InformacionUsuario, on_delete=models.DO_NOTHING, verbose_name='Usuario')
    anime = models.ForeignKey(Anime, on_delete=models.DO_NOTHING, verbose_name='Anime')
    fechaCalificacion = models.DateField(null=True, blank=True, verbose_name='Fecha de Calificación')
    calificacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name='Calificación')
    def __str__(self):
        return str(self.calificacion)