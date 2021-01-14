from random import randrange


#
## CREACIÓN DE USUARIOS PARA EL SISTEMA DE RECOMENDACIÓN
#

def numAGenero(num):
    return {
             1 : 'F',
             2 : 'M'
    }[num]

def numAPostalCode(num):
    return {
            1: 29009,
            2: 41020,
            3: 41600,
            4: 29035,
            5: 28015,
            6: 28013,
            7: 5200,
            8: 47210,
            9: 17009,
            10: 29013,
            11: 41019,
            12: 41600,
            13: 28015,
            14: 28013,
            15: 5223,
            16: 47210,
            17: 47207
        
    }[num]

def create_usersfile(num_usuarios):
    
    users = open("users", "w")
    
    # Rango del número de usuarios
    for i in range(1,num_usuarios+1):
        
        lista = []
        lista.append(str(i))                                            # Indice del documento
        lista.append(str(randrange(10,50)))                             # Índice del la edad
        lista.append(str(numAGenero(randrange(1,3))))                   # Género 
        lista.append(str(numAPostalCode(randrange(1,18))))              # Código Postal
        linea = '|'.join(lista)
        users.write(linea + "\n")
    
    users.close()
    
    
create_usersfile(100)