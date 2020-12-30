from random import randrange
import datetime
import os

def random_date():
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


## CREAMOS UN ARCHIVO DE TEST Y CREAMOS ALEATORIAMENTE LOS DATOS

test = open("test", "w")

# Rango del número de usuarios
for i in range(1,20+1):
    #Rango del número de calificaciones por usuario
    for j in range(1,6):
        lista = []
        lista.append(str(i))                    # Indice de los usuarios
        lista.append(str(randrange(50)+1))      # Índice del anime, rango por número de animes
        lista.append(str(random_date()))        # Fecha de calificación
        lista.append(str(randrange(11)))        # Calificación, rango de 0 a 10
        linea = '|'.join(lista)
        test.write(linea + "\n")

test.close()

## AÑADIMOS A UN DICCIONARIO CADA LINEA Y LAS CONTAMOS

lista1 = []

fileobj=open(r"C:\Users\PedroC\git\proyectoaii\data\test", "r")
for line in fileobj.readlines():
    rip = line.split('|')
    if len(rip) != 4:
        continue
    usuario=rip[0].strip() 
    anime=rip[1].strip() 
    fecha=rip[2].strip()
    valoracion=rip[3].strip()
    
    lista1.append(int(anime))

numberOcc = dict(sorted((i, lista1.count(i)) for i in lista1))
print("AAAAAAAAAAA")
print(numberOcc)

## CORREGIMOS LOS POSIBLES ANIMES QUE NO TENGAN VALORACION NINGUNA

# Rango del número de animes
for i in range(1,51):
    try:
        # Checkea si existe. Si no existe salta un error y creamos un par de entradas
        numberOcc[i]
        
        if numberOcc[i] == 1:
            test = open("test", "a")
            for ij in range(0,randrange(1,3)):
                lista = []
                lista.append(str(randrange(20)))        # Indice de los usuarios
                lista.append(str(i))                    # Índice del anime
                lista.append(str(random_date()))        # Fecha de calificación
                lista.append(str(randrange(11)))        # Calificación
                linea = '|'.join(lista)
        
                test.write(linea + "\n")
                print("Created for: " + str(i))
            test.close()
        
    except KeyError:
        test = open("test", "a")
        for ij in range(0,randrange(1,3)):
            lista = []
            lista.append(str(randrange(20)))        # Indice de los usuarios
            lista.append(str(i))                    # Índice del anime
            lista.append(str(random_date()))        # Fecha de calificación
            lista.append(str(randrange(11)))        # Calificación
            linea = '|'.join(lista)
        
            test.write(linea + "\n")
        test.close()
        
## EXPORTAMOS AL ARCHIVO FINAL INDEXANDO CADA ENTRADA

with open("test", "r") as a, open("data", "w") as b:
    index = 1
    for line in a:
        b.write("{:d}|{}\n".format(index, line.rstrip()))
        index += 1

## CONTAMOS DE NUEVO LOS ANIMES PARA COMPROBAR QUE NO TENGAN ERRORES

lista2 = []

fileobj=open(r"C:\Users\PedroC\git\proyectoaii\data\data", "r")
for line in fileobj.readlines():
    rip = line.split('|')
    if len(rip) != 5:
        continue
    id_u=rip[0].strip()
    usuario=rip[1].strip() 
    anime=rip[2].strip() 
    fecha=rip[3].strip()
    valoracion=rip[4].strip()
    
    lista2.append(int(anime))

numberOcc = dict(sorted((i, lista2.count(i)) for i in lista2))
print("BBBBBBBBBBBBB")
print(numberOcc)

test.close()
os.remove("test")
