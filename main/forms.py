#encoding:utf-8
from django import forms
from main.models import Genero

class BusquedaPorFechaInicioForm(forms.Form):
    fecha = forms.DateField(label="Fecha (Formato yyyy-mm-dd)", widget=forms.DateInput(format='%Y/%m/%d'), required=True)
    
class BusquedaPorGeneroForm(forms.Form):
    lista=[(g.id,g.nombre) for g in Genero.objects.all()]
    genero = forms.ChoiceField(label="Seleccione el género", choices=lista)
    
class BusquedaPorSinopsisForm(forms.Form):
    sinopsis = forms.CharField(label="Palabras de la sinopsis a buscar (En inglés)", widget=forms.TextInput())
    
class UsuarioForm(forms.Form):
    id = forms.CharField(label='ID de Usuario')
    
class AnimeForm(forms.Form):
    id = forms.CharField(label='ID del Anime')