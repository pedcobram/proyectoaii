# -*- coding: utf-8 -*-


import urllib.request
import datetime
import os

from main.models import Anime, Genero
from main.forms import BusquedaPorFechaInicioForm, BusquedaPorGeneroForm, BusquedaPorSinopsisForm

from django.shortcuts import render, redirect

from bs4 import BeautifulSoup

from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, DATETIME, KEYWORD
from whoosh.qparser import QueryParser
from whoosh import qparser
from whoosh.filedb.filestore import FileStorage
from pickle import NONE

dirindex = r"C:\Users\PedroC\git\proyectoaii\Index"

def monthToNum(shortMonth):

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
    }[shortMonth]

def get_schema():
    return Schema(titulo=TEXT(stored=True), imagen=TEXT(stored=True), rango_web=TEXT(stored=True), 
                  popularidad=TEXT(stored=True), fecha_inicio=DATETIME(stored=True), fecha_final=DATETIME(stored=True), 
                  episodios=TEXT(stored=True), sinopsis=TEXT(stored=True), generos=KEYWORD(stored=True))

def populateDB(i):
    
    if i == 0:
        num_animes = 0
        num_generos = 0
        Anime.objects.all().delete()
        
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
                fecha_inicio = datetime.datetime(int(emision[2]), monthToNum(emision[0]), int(emision[1].split(',')[0])).strftime("%Y-%m-%d")
            if(len(emision) > 5):
                fecha_final = datetime.datetime(int(emision[6]), monthToNum(emision[4]), int(emision[5].split(',')[0])).strftime("%Y-%m-%d")
            
            lista_generos = s.find("td", class_="borderClass").next_element.find_all('span', itemprop="genre")
            
            lista = []
            for genero in lista_generos:
                lista.append(genero.text)
            lista_generos_comas = ",".join(lista)
            
        except UnicodeEncodeError:
            continue
        
        lista_generos_obj = []
        for genero in lista_generos:
            genero_obj, created = Genero.objects.get_or_create(nombre=genero.text)
            lista_generos_obj.append(genero_obj)
            if created:
                num_generos += 1       
                
        a = Anime.objects.create(titulo=titulo, imagen=imagen, rango=rango_web, popularidad=popularidad_web, episodios=episodios, sinopsis=sinopsis, fechaInicio=fecha_inicio, fechaFinal=fecha_final)
        
        for genero in lista_generos_obj:
            a.generos.add(genero)
        
        writer.add_document(titulo=titulo, imagen=imagen, rango_web=rango_web, popularidad=popularidad_web, fecha_inicio=fecha_inicio, fecha_final=fecha_final, episodios=episodios, sinopsis=sinopsis, generos=lista_generos_comas)
        
        num_animes += 1
    
    writer.commit()
      
    return ((num_animes, num_generos))
    
def carga(request):
    
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            for i in range(0,1):
                num_animes, num_generos = populateDB(i)
                num_generos = Genero.objects.all().count()
            mensaje="Se han almacenado " + str(num_animes) + " animes y " + str(num_generos) + " géneros"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def index(request): 
    num_animes = Anime.objects.all().count()
    num_generos = Genero.objects.all().count()
    return render(request,'inicio.html', {'num_animes':num_animes, 'num_generos':num_generos})

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
    
    
    
    