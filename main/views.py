# -*- coding: utf-8 -*-

import urllib.request
import datetime
import os
import shelve

from main.models import Anime, Genero, InformacionUsuario, Calificacion
from main.forms import BusquedaPorFechaInicioForm, BusquedaPorGeneroForm, BusquedaPorSinopsisForm, UsuarioForm, AnimeForm
from django.shortcuts import render, redirect, get_object_or_404
from main.recommendations import getRecommendations, transformPrefs, topMatches
#from data import createDataFile, createUserFile

from bs4 import BeautifulSoup

from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, DATETIME, KEYWORD
from whoosh.qparser import QueryParser
from whoosh import qparser
from whoosh.filedb.filestore import FileStorage
from django.http.response import Http404

dirindex = r"C:\Users\PedroC\git\proyectoaii\Index"

def mesANum(mes):
    return {
            'Jan' : 1,
            'Feb' : 2,
            'Mar' : 3,
            'Apr' : 4,
            'May' : 5,
            'Jun' : 6,
            'Jul' : 7,
            'Aug' : 8,
            'Sep' : 9, 
            'Oct' : 10,
            'Nov' : 11,
            'Dec' : 12
    }[mes]

def cargarDiccionario():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS1.dat")
    ratings = Calificacion.objects.all()
    for ra in ratings:
        user = int(ra.usuario.id)
        itemid = int(ra.anime.id)
        rating = float(ra.calificacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf.close()

def get_schema():
    return Schema(titulo=TEXT(stored=True), imagen=TEXT(stored=True), rango_web=TEXT(stored=True), 
                  popularidad=TEXT(stored=True), fecha_inicio=DATETIME(stored=True), fecha_final=DATETIME(stored=True), 
                  episodios=TEXT(stored=True), sinopsis=TEXT(stored=True), generos=KEYWORD(stored=True))


def deleteCompleteBD():
    Calificacion.objects.all().delete()
    InformacionUsuario.objects.all().delete()
    Genero.objects.all().delete()
    Anime.objects.all().delete()

def populateDB(i):
 
    if i == 0:
        deleteCompleteBD()
        
        
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
        create_in(dirindex, schema=get_schema())   
        
    ix = FileStorage(dirindex).open_index()
    
    writer = ix.writer()
        
    f = urllib.request.urlopen("https://myanimelist.net/topanime.php?limit=" + str(50*i))
    s = BeautifulSoup(f, "html.parser")
    lista_animes = s.find("table", class_="top-ranking-table").find_all("a", class_="hoverinfo_trigger fl-l ml12 mr8")
    for lista_anime in lista_animes:
        
        ix = FileStorage(dirindex).open_index()
        
        try:
            f = urllib.request.urlopen(lista_anime['href'])
            s = BeautifulSoup(f, "html.parser")            
            
            titulo = s.find("h1", class_="title-name h1_bold_none").text
            
            imagen = s.find("td", class_="borderClass").next_element.next_element.next_element.find('img')['data-src']
        
            rango_web = s.find("div", class_="di-ib ml12 pl20 pt8").contents[0].text.split()[1]
        
            popularidad_web = s.find("div", class_="di-ib ml12 pl20 pt8").contents[1].text.split()[1]
        
            emision = ''.join(s.find("td", class_="borderClass").next_element.find_all('div', class_="spaceit")[1].stripped_strings)[6:].split()
            
            episodios = ''.join(s.find("td", class_="borderClass").next_element.find_all('div', class_="spaceit")[0].stripped_strings)[9:]
            
            sinopsis = s.find("p").text
            
            if(len(emision) > 0):
                fecha_inicio = datetime.datetime(int(emision[2]), mesANum(emision[0]), int(emision[1].split(',')[0])).strftime("%Y-%m-%d")
            if(len(emision) > 5):
                fecha_final = datetime.datetime(int(emision[6]), mesANum(emision[4]), int(emision[5].split(',')[0])).strftime("%Y-%m-%d")
            
            lista_generos = s.find("td", class_="borderClass").next_element.find_all('span', itemprop="genre")
            
            lista = []
            for genero in lista_generos:
                lista.append(genero.text)
            lista_generos_comas = ",".join(lista)
            
        except UnicodeEncodeError:
            continue
        
        lista_generos_obj = []
        for genero in lista_generos:
            genero_obj, _ = Genero.objects.get_or_create(nombre=genero.text)
            lista_generos_obj.append(genero_obj)       
        
        id_u = Anime.objects.all().count() + 1     
        a = Anime.objects.create(id=id_u, titulo=titulo, imagen=imagen, rango=rango_web, popularidad=popularidad_web, episodios=episodios, sinopsis=sinopsis, fechaInicio=fecha_inicio, fechaFinal=fecha_final)
        
        for genero in lista_generos_obj:
            a.generos.add(genero)
        
        writer.add_document(titulo=titulo, imagen=imagen, rango_web=rango_web, popularidad=popularidad_web, fecha_inicio=fecha_inicio, fecha_final=fecha_final, episodios=episodios, sinopsis=sinopsis, generos=lista_generos_comas)
    
    writer.commit()
      
    return None

def popularUsuarios():
    lista=[]
    dict={}
    fileobj=open(r"C:\Users\PedroC\git\proyectoaii\data\users", "r")
    for line in fileobj.readlines():
        rip = line.split('|')
        if len(rip) != 4:
            continue
        id_u=int(rip[0].strip())
        u=InformacionUsuario(id=id_u, edad=rip[1].strip(), genero=rip[2].strip(), codigoPostal=rip[3].strip())
        lista.append(u)
        dict[id_u]=u
    fileobj.close()
    InformacionUsuario.objects.bulk_create(lista)

    return(dict)

def popularCalificaciones():
    lista=[]
    dict={}
    fileobj=open(r"C:\Users\PedroC\git\proyectoaii\data\data", "r")
    for line in fileobj.readlines():
        rip = line.split('|')
        if len(rip) != 5:
            continue    
        id_u=int(rip[0].strip())
        usuario = InformacionUsuario.objects.get(id=rip[1].strip())
        anime = Anime.objects.get(id=rip[2].strip()) 
        u=Calificacion(id=id_u, usuario=usuario, anime=anime, fechaCalificacion=rip[3].strip(), calificacion=rip[4].strip())
        lista.append(u)
        dict[id_u]=u
    fileobj.close()
    Calificacion.objects.bulk_create(lista)

    return(dict)
  
def carga(request):
    
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            for i in range(0,2):
                populateDB(i)
            num_animes = Anime.objects.all().count()
            num_generos = Genero.objects.all().count()
            mensaje="Se han almacenado " + str(num_animes) + " animes y " + str(num_generos) + " géneros"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def index(request): 
    num_animes = Anime.objects.all().count()
    num_generos = Genero.objects.all().count()
    num_usuarios = InformacionUsuario.objects.all().count()
    num_calificaciones = Calificacion.objects.all().count()
    return render(request,'inicio.html', {'num_animes':num_animes, 'num_generos':num_generos, 'num_usuarios':num_usuarios, 'num_calificaciones':num_calificaciones})

def lista_animes(request):
    animes = Anime.objects.all()
    return render(request,'animes.html', {'animes':animes})

def buscar_animesporfechainicio(request):
    formulario = BusquedaPorFechaInicioForm()
    animes = None
    
    if request.method=='POST':
        formulario = BusquedaPorFechaInicioForm(request.POST)      
        if formulario.is_valid():
            animes = Anime.objects.filter(fechaInicio__gte=formulario.cleaned_data['fecha'])
            
    return render(request, 'animesbusquedaporfechainicio.html', {'formulario':formulario, 'animes':animes})

def buscar_animesporgenero(request):
    formulario = BusquedaPorGeneroForm()
    animes = None
    
    if request.method=='POST':
        formulario = BusquedaPorGeneroForm(request.POST)      
        if formulario.is_valid():
            genero=Genero.objects.get(id=formulario.cleaned_data['genero'])
            animes = genero.anime_set.all()
            
    return render(request, 'animesbusquedaporgenero.html', {'formulario':formulario, 'animes':animes})

def buscar_animesporsinopsis(request):
    formulario = BusquedaPorSinopsisForm(request.POST)
    lista_animes = []
    
    if formulario.is_valid():
        ix = FileStorage(dirindex).open_index()
        query = QueryParser("sinopsis", ix.schema, group=qparser.AndGroup).parse(formulario.cleaned_data['sinopsis'])
        with ix.searcher() as searcher:
            results = searcher.search(query)
            for r in results:
                anime = []
                anime.append(r['titulo'])
                anime.append(r['imagen'])
                anime.append(r['rango_web'])
                anime.append(r['popularidad'])
                anime.append(r['fecha_inicio'])
                anime.append(r['fecha_final'])
                anime.append(r['episodios'])
                anime.append(r['sinopsis'])
                anime.append(r['generos'])
                lista_animes.append(anime)
                
    return render(request, 'animesbusquedaporsinopsis.html', {'formulario':formulario, 'animes':lista_animes})

def cargar_usuarios_y_calificaciones(request):
    if request.method=='POST':
        if 'Aceptar' in request.POST:
            Calificacion.objects.all().delete()
            InformacionUsuario.objects.all().delete()
            
            popularUsuarios()
            popularCalificaciones()
            cargarDiccionario()
            
            num_usuarios = InformacionUsuario.objects.all().count()
            num_calificaciones = Calificacion.objects.all().count()
            mensaje="Se han almacenado " + str(num_usuarios) + " usuarios y " + str(num_calificaciones) + " calificaciones"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacionusuarioscalificaciones.html')

def recomendar_animes_usuario(request):
    mensaje = None
    if request.method=='GET':
        form = UsuarioForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            
            try:
                user = get_object_or_404(InformacionUsuario, pk=idUser)
            except Http404:
                mensaje = 'No existe ningún usuario con el ID seleccionado'
                return render(request, 'busquedaporusuarios.html', {'form':form, 'mensaje':mensaje})
                 
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUser))
            recommended = rankings[:2]
            anime = []
            scores = []
            for re in recommended:
                anime = Anime.objects.filter(pk=re[1])
                scores.append(re[0])
            animes = zip(anime,scores)
            
            animes_cal = []
            for a in Calificacion.objects.filter(usuario=user):
                animes_cal.append(a)
            
            return render(request,'recomendacionanimes.html', {'user': user, 'animes_recom': animes, 'animes_cal': animes_cal})
    form = UsuarioForm()
    return render(request,'busquedaporusuarios.html', {'form': form})
  
def buscar_animessimilares(request):
    anime = None
    mensaje = None
    if request.method=='GET':
        form = UsuarioForm(request.GET, request.FILES)
        if form.is_valid():
            idAnime = form.cleaned_data['id']
            
            try:
                anime = get_object_or_404(Anime, pk=idAnime)
            except Http404:
                mensaje = 'No existe ningún anime con el ID seleccionado'
                return render(request, 'buscaranimessimilares.html', {'form':form, 'mensaje':mensaje})
                
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idAnime),n=3)
            anime = []
            similar = []
            for re in recommended:
                anime.append(Anime.objects.get(pk=re[1]))
                similar.append(re[0])
            animes= zip(anime,similar)

            return render(request,'animessimilares.html', {'anime': anime,'animes': animes})
        
    form = AnimeForm()
    return render(request,'buscaranimessimilares.html', {'form': form})  