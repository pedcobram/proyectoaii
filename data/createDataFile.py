from random import randrange
import datetime

def random_date():
    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.date(2020, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date

def create_datafile(num_usuarios, num_calificaciones, num_anime):
    ## CREAMOS UN ARCHIVO DE TEST Y CREAMOS ALEATORIAMENTE LOS DATOS
    test = open("test", "w")
    
    # Rango del número de usuarios
    for i in range(1,num_usuarios+1):
        #Rango del número de calificaciones por usuario
        for _ in range(1,num_calificaciones+1):
            lista = []
            lista.append(str(i))                            # Indice de los usuarios
            lista.append(str(randrange(num_anime)+1))       # Índice del anime, rango por número de animes
            lista.append(str(random_date()))                # Fecha de calificación
            lista.append(str(randrange(11)))                # Calificación, rango de 0 a 10
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
        anime=rip[1].strip() 
        
        lista1.append(int(anime))
    
    numberOcc = dict(sorted((i, lista1.count(i)) for i in lista1))
    
    ## CORREGIMOS LOS POSIBLES ANIMES QUE NO TENGAN VALORACION NINGUNA
    # Rango del número de animes
    for i in range(1,num_anime+1):
        try:
            # Checkea si existe. Si no existe salta un error y creamos un par de entradas
            numberOcc[i]
            
            if numberOcc[i] == 1:
                test = open("test", "a")
                for _ in range(1,randrange(1,3)):
                    lista = []
                    lista.append(str(randrange(num_usuarios+1)))          # Indice de los usuarios
                    lista.append(str(i))                                # Índice del anime
                    lista.append(str(random_date()))                    # Fecha de calificación
                    lista.append(str(randrange(11)))                    # Calificación
                    linea = '|'.join(lista)
            
                    test.write(linea + "\n")
                    #print("Created for: " + str(i))
                test.close()
            
        except KeyError:
            test = open("test", "a")
            for _ in range(1,randrange(1,3)):
                lista = []
                lista.append(str(randrange(num_usuarios+1)))          # Indice de los usuarios
                lista.append(str(i))                                # Índice del anime
                lista.append(str(random_date()))                    # Fecha de calificación
                lista.append(str(randrange(11)))                    # Calificación
                linea = '|'.join(lista)
            
                test.write(linea + "\n")
            test.close()
            
    ## EXPORTAMOS AL ARCHIVO FINAL INDEXANDO CADA ENTRADA
    with open("test", "r") as a, open("data", "w") as b:
        index = 1
        for line in a:
            b.write("{:d}|{}\n".format(index, line.rstrip()))
            index += 1  
    
num_usuarios = 100
num_calificaciones = 20
num_anime = 49

create_datafile(num_usuarios, num_calificaciones, num_anime)

