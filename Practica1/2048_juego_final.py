"Abad Hernández Javier\
Castro García Jaime\
Grugo T3, Grupo de practicas Y8"

import random
import copy

"""Se ejecuta siempre, se encarga de imprimir los menus, y de llamar a otras funciones, se ejecuta siempre al principio
del programa y tambien cuando la jugada elegida sea [F]inalizar. Contiene la parte importante del código, la que se 
encarga de ejecutar todo lo demás."""
def main():
    print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐  CLON-3  ‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐ ")
    print("‐ Práctica de Paradigmas de Programación 2019‐20 ‐ ")
    print("‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐ ")
    print("1. CREAR NUEVO TABLERO"+"\n"+"2. LEER TABLERO DEL FICHERO"+"\n"+"3. SALIR", "\n")



#Dependiendo de lo elegido en eleccion_one creara todo desde 0, leera el fichero, o terminara la ejecución del programa
#por completo.

    eleccion_one = int(input("Indique opción:"))
    if eleccion_one == 1:
        print("--------¡QUE COMIENCE EL JUEGO!---------")
        print("Indique opción:", eleccion_one)
        dimension = int(input("Tamaño del tablero: "))
        modo = 1
        obstaculos = int(input("Número de obstáculos: "))
        matriz = []
        for i in range(dimension):
            matriz.append([])
            for j in range(dimension):
                matriz[i].append(0)
        introducir_nuevo_elemento = True
    # lectura de fichero
    elif eleccion_one == 2:

        fichero = False
        while fichero != True:
            try:
                nombre = input("Nombre del fichero, por ejemplo:(juego.txt): ")
                archivo_texto = open(nombre, "r")
                lineas_fichero = archivo_texto.readlines()
                fichero = True

            except FileNotFoundError:
                print("Fichero no encontrado, pruebe con otro")

        dimension = lineas_fichero.__len__() - 2
        matriz = []
        for i in range(dimension):
            matriz.append([])
            for j in range(dimension):
                matriz[i].append(0)
        movimientos = int(lineas_fichero[0]) #movimientos en la 1º lína del fichero
        puntos = int(lineas_fichero[1]) #puntuación en la 2º línea del fichero
        modo = 1  #el modo de apertura es siempre el 1
        num_alfabeto = diccionario(modo)
        lista = list(num_alfabeto.values())
        index = 1

        for i in range(dimension):
            index += 1
            for j in range(dimension):
                if lineas_fichero[index][j] == "*":
                    matriz[i][j] = "*"
                if lineas_fichero[index][j] != "*" and lineas_fichero[index][j] != ".":
                    valor = lineas_fichero[index][j]
                    posicion = lista.index(valor)
                    matriz[i][j] = posicion + 1

        archivo_texto.close()
        movimientos = int(movimientos)
        puntos = int(puntos)
        introducir_nuevo_elemento = False
    else:
        print("---------------------------------------------------")
        print("---------------¡¡Hasta la próxima!!----------------")
        print("---------------------------------------------------")
        exit()
    #Se crea el tablero inicial con sus elementos iniciales"""
    if eleccion_one == 1:
        matriz = crear_obstaculo(matriz, obstaculos,dimension)
        puntos = 0
        movimientos = 0

    jugada = ""
    while True:

        num_alfabeto = diccionario(modo)
        #Aquí se encarga de meter un nuevo elemento siempre que se elija una jugada de las de movimiento
        if movimientos != -1 and introducir_nuevo_elemento == True:
            mostrar_tablero(dimension, modo, matriz, num_alfabeto)
            continuar = input("Pulse [Enter] para mostrar inserción del nuevo bloque")
            print("MOVIMIENTOS: ", str(movimientos), "|", "PUNTUACIÓN: ", str(puntos), "\n")
            if continuar == '':

                matriz = nuevo_elemento(matriz,dimension)

        introducir_nuevo_elemento = True

        while jugada not in ("s", "b", "i", "d", "f", "g", "m"):

            mostrar_tablero(dimension, modo, matriz, num_alfabeto)
            print("MOVIMIENTOS: ", str(movimientos), "|", "PUNTUACIÓN: ", str(puntos), "\n" )

            jugada = input("[S]ubir, [B]ajar, [I]zquierda, [D]erecha | [M]odo | [G]uardar, [F]in: ").lower() #Coge tanto mayusculas como minusculas

            if jugada == "s" or jugada == "d" or jugada == "i" or jugada == "b":
                movimientos = movimientos + 1


        else:
            if jugada == "d":
                matriz, puntos = movimiento_derecha(matriz, puntos, num_alfabeto)
                jugada = ""

            elif jugada == "i":
                matriz, puntos = movimiento_izquierda(matriz, puntos, num_alfabeto)
                jugada = ""

            elif jugada == "s":
                matriz, puntos = movimiento_arriba(matriz, puntos, num_alfabeto)
                jugada = ""

            elif jugada == "b":
                matriz, puntos = movimiento_abajo(matriz, puntos, num_alfabeto)
                jugada = ""

            elif jugada == "f":
                print("----------PARTIDA TERMINADA----------")
                print("MOVIMIENTOS TOTALES: ", movimientos, "|" , "PUNTUACIÓN TOTAL: ", puntos ,"\n\n")
                main() #Llamamiento al main cuando el usuario pulse F, para empezar en el menu principal

            elif jugada == "m":
                print("ESCOJA MODO DE VISUALIZACIÓN: "+"\n1. Alfabeto\n2. Nivel\n3. 1024\n4. 2048")
                modo = int(input("Elija opción: "))
                jugada = ""
                introducir_nuevo_elemento = False

            elif jugada == "g":
                guardar_fichero(movimientos, puntos, dimension, matriz)
                jugada = ""

        if  ganador(matriz) == True:
            print("----------HAS GANADO----------")

        if len(casillas_vacias(matriz)) == 0 and sin_movimientos(matriz) == True:
            print("----------HAS PERDIDO----------")
            print("MOVIMIENTOS TOTALES: ", movimientos, "|" ,"PUNTUACIÓN TOTAL: ", puntos )
            break

"Imprime el tablero en función del modo seleccioado por el usuario, con el tamaño correspondiente. La impesión es con" \
" 0´s y matrix transforma los 0´s en blancos. "

def mostrar_tablero(dimension, modo, matriz, num_alfabeto):
    matrix = copy.deepcopy(matriz)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                matrix[i][j] = " "

    if modo == 3 or modo == 4:
        for i in range(dimension):
            for j in range(0, dimension):
                print("+----", end="")
            print("+")
            for j in range(0, dimension):
                if matriz[i][j] == "*": #Se generalia "*" para cualquier modo de juego, ya que se pintan diferente en función del modo
                    print("|", '****', end="", sep='')
                elif matrix[i][j] == ' ':
                    print('|%4s' % matrix[i][j], end="", sep='')
                else:
                    aux = matriz[i][j]  #Implementación para poder realizar el cambio de modo siempre que el usuario lo pida
                    print('|%4s' % num_alfabeto[aux], end="", sep='')

            print("|")

        for i in range(dimension):
            print("+----", end="")
        print("+")
    elif modo == (2):
        for i in range(dimension):
            for j in range(dimension):
                print("+--", end="")
            print("+")
            for j in range(dimension):
                if matriz[i][j] == "*":
                    print("|", '**', end="", sep='')
                elif matrix[i][j] == ' ':
                    print('|%2s' % matrix[i][j], end="", sep='')
                else:
                    aux = matriz[i][j]
                    print('|%2s' % num_alfabeto[aux], end="", sep='')
            print("|")
        for i in range(dimension):
            print("+--", end="")
        print("+")

    else:
        for i in range(dimension):
            for j in range(dimension):
                print("+-", end="")
            print("+")
            for j in range(dimension):
                if matriz[i][j] == "*":
                    print("|", '*', end="", sep='')
                elif matrix[i][j] == ' ':
                    print('|%1s' % matrix[i][j], end="", sep='')
                else:
                    aux = matriz[i][j]
                    print('|%1s' % num_alfabeto[aux], end="", sep='')
            print("|")
        for i in range(dimension):
            print("+-", end="")
        print("+")

"""Tenemos un unico diccionario que varía para los diferentes modos de juego. Inicialmente.
 El resto de los modos simplemente cambian el modo de representar el diccionario,
y lo podremos pedir después a medida que avancemos en el juego."""

def diccionario(modo):
    if modo == 1:
        num_alfabeto = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I',
                        10: 'J', 11: 'K', 12: 'L'}

    elif modo == 2:
        num_alfabeto = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
                        10: '10', 11: '11', 12: '12'}

    elif modo == 3:
        num_alfabeto = {1: '1', 2: '2', 3: '4', 4: '8', 5: '16', 6: '32', 7: '64', 8: '128',
                        9: '256', 10: '512', 11: '1024', 12: '2048'}

    elif modo == 4:
        num_alfabeto = {1: '2', 2: '4', 3: '8', 4: '16', 5: '32', 6: '64', 7: '128', 8: '256',
                        9: '512', 10: '1024', 11: '2048', 12: '4096'}


    return num_alfabeto

""" Función que se encargaraa de introducir o el primer o el segundo elemento del diccionario a la matriz, 
dependiendo de si encuentra obstaculo o 0's en la matriz. Si no encuentra obstaculos, imprimirá con un 25% 
de posibilidades el segundo elemento del diccionario y con un 75% el primer elemento del diccionario.
"""
def nuevo_elemento(matriz,dimension):
    num_aleat = random.randrange(100)
    hay_obstaculo = True
    espacios_vacios=casillas_vacias(matriz)
    if len(espacios_vacios)==0:
        return matriz
    while hay_obstaculo:
        posx_aleat = random.randrange(0, dimension)
        posy_aleat = random.randrange(0, dimension)
        if matriz[posx_aleat][posy_aleat] == "*":
            hay_obstaculo = True

        elif matriz[posx_aleat][posy_aleat] == 0:
            if num_aleat < 75:
                nuevo_elemento = 1
            else:
                nuevo_elemento = 2
            matriz[posx_aleat][posy_aleat] = nuevo_elemento
            hay_obstaculo = False

    return matriz

"""
Función que se encarga de imprimir en la matriz obstaculos de manera random comprobando antes siempre si hay ya otro 
obstaculo en esa posición.
"""
def crear_obstaculo(matriz, obstaculos,dimension):
    for a in range(obstaculos):
        existe = True
        while existe:
            posx_aleat = random.randrange(0, dimension)
            posy_aleat = random.randrange(0, dimension)
            if matriz[posx_aleat][posy_aleat] == "*":
                existe = True
            else:
                matriz[posx_aleat][posy_aleat] = "*"
                existe = False


    return matriz

"""Función que se encarga de recorrer toda la matriz, para ver si hay si hay 0's en la matriz, que es lo correspondiente
a los espacios en blanco del tablero. """
def casillas_vacias(matriz):
    vacias = []
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == 0:
                vacias.append([i, j])
    return vacias

"""Función que cada vez que hay una fusión suma de puntuación la posición + 1 a la que corresponde en el diccionario el
resultdado de esa suma, teniendo en cuenta que la primera posición es la 0.
"""
def puntuacion(valor_num, puntos, num_alfabeto):
    lista = list(num_alfabeto.keys())
    posicion = lista.index(valor_num) + 1
    puntos = puntos + posicion

    return puntos

"""Función que se encarga de realizar los movimientos, y la fusion de los elementos del diccionario, hacia la derecha.
Comprobando primero si hay fusión disponible y si no hay obstaculo"""
def movimiento_derecha(matrix, puntos, num_alfabeto):
    for i in range(len(matrix)):
        mezclas = []
        for x in range(len(matrix) - 1):
            for j in range(-2, -len(matrix) - 1, -1):

                if matrix[i][j] != "*" and matrix[i][j] != 0 and matrix[i][j + 1] == 0:
                    matrix[i][j + 1] = matrix[i][j]
                    matrix[i][j] = 0


                elif matrix[i][j] != "*" and matrix[i][j] != 0 and matrix[i][j] == matrix[i][
                    j + 1] and j not in mezclas and j - 1 not in mezclas:
                    matrix[i][j + 1] += 1 #se suma 1, por como esta estructurado el diccionario
                    valor_num = matrix[i][j + 1]
                    puntos = puntuacion(valor_num, puntos, num_alfabeto)
                    matrix[i][j] = 0
                    mezclas.append(j)

    return matrix, puntos

"""Función que se encarga de realizar los movimientos, y la fusion de los elementos del diccionario, hacia la izquierda.
Comprobando primero si hay fusión disponible y si no hay obstaculo"""
def movimiento_izquierda(matrix, puntos, num_alfabeto):
    for i in range(len(matrix)):
        mezclas = []
        for x in range(len(matrix) - 1):
            for j in range(1, len(matrix)):
                if matrix[i][j] != "*" and matrix[i][j] != 0 and matrix[i][j - 1] == 0:
                    matrix[i][j - 1] = matrix[i][j]
                    matrix[i][j] = 0

                elif matrix[i][j] != "*" and matrix[i][j] != 0 and matrix[i][j] == matrix[i][
                    j - 1] and j not in mezclas and j + 1 not in mezclas:
                    matrix[i][j - 1] += 1
                    valor_num = matrix[i][j - 1]
                    puntos = puntuacion(valor_num, puntos, num_alfabeto)
                    matrix[i][j] = 0
                    mezclas.append(j)

    return matrix, puntos

"""Función que se encarga de realizar los movimientos, y la fusion de los elementos del diccionario, hacia la abajo.
Comprobando primero si hay fusión disponible y si no hay obstaculo"""
def movimiento_abajo(matrix, puntos, num_alfabeto):
    for j in range(len(matrix)):
        mezclas = []
        for x in range(len(matrix) - 1):
            for i in range(-2, -len(matrix) - 1, -1):
                if matrix[i][j] != "*" and matrix[i][j] != 0 and matrix[i + 1][j] == 0:
                    matrix[i + 1][j] = matrix[i][j]
                    matrix[i][j] = 0

                elif matrix[i][j] != "*" and matrix[i][j] != 0 and matrix[i][j] == matrix[i + 1][
                    j] and i not in mezclas and i - 1 not in mezclas:
                    matrix[i + 1][j] += 1
                    valor_num = matrix[i + 1][j]
                    puntos = puntuacion(valor_num, puntos, num_alfabeto)
                    matrix[i][j] = 0
                    mezclas.append(i)

    return matrix, puntos

"""Función que se encarga de realizar los movimientos, y la fusion de los elementos del diccionario, hacia la arriba.
Comprobando primero si hay fusión disponible y si no hay obstaculo"""
def movimiento_arriba(matrix, puntos, num_alfabeto):
    for j in range(len(matrix)):
        mezclas = []
        for x in range(len(matrix) - 1):
            for i in range(1, len(matrix)):
                if matrix[i][j] != "*" and matrix[i][j] != 0 and matrix[i - 1][j] == 0:
                    matrix[i - 1][j] = matrix[i][j]
                    matrix[i][j] = 0

                elif matrix[i][j] != "*" and matrix[i][j] != 0 and matrix[i][j] == matrix[i - 1][
                    j] and i not in mezclas and i + 1 not in mezclas:
                    matrix[i - 1][j] += 1
                    valor_num = matrix[i - 1][j]
                    puntos = puntuacion(valor_num, puntos, num_alfabeto)
                    matrix[i][j] = 0
                    mezclas.append(i)

    return matrix, puntos

"Función que recorre la matriz y comprueba si quedan movimientos posibles comparando la matriz actual, " \
"con otra que contenga una posible fusiónn"

def sin_movimientos(matriz):
    final = True
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == "0":
                final = False
                return final

    for i in range(len(matriz)):
        for j in range(len(matriz) - 1):
            if matriz[i][j] == matriz[i][j + 1] and matriz[i][j]!="*":
                final = False

    for i in range(len(matriz) - 1):
        for j in range(len(matriz)):
            if matriz[i][j] == matriz[i + 1][j] and matriz[i][j]!="*":

                final = False

    return final

"""Función que se encarga de ver si has llegado al elemento correspondiente a la posición 10 y/o -2 del diccionario
es decir, la correspondiente """
def ganador(matriz):
    mostrar_ganador = False

    for i in range(len(matriz)):
        for j in range (len(matriz[0])):
            if matriz[i][j]==11:
                mostrar_ganador = True

    return mostrar_ganador

"""Función que se encarga de guardar en un fichero lo que llevamos hasta el momento en el que se ejecute esta opción
de juego, con la puntuación, los movimientos y el tablero."""
def guardar_fichero(movimientos, puntos,dimension, matriz):
    num_alfabeto = diccionario(1)
    nombre = input("Nombre del fichero, por ejemplo:(juego.txt): ")
    archivo_texto = open(nombre, "w")

    archivo_texto.write(str(movimientos))
    archivo_texto.write("\n")
    archivo_texto.write(str(puntos))
    archivo_texto.write("\n")

    for i in range(dimension):
        for j in range(dimension):

            if matriz[i][j] == 0:
                vacio = '.'
                archivo_texto.write(vacio)
            elif matriz[i][j] == "*":
                asterisco = "*"
                archivo_texto.write(asterisco)
            elif matriz[i][j] != 0 and matriz[i][j] != "*":
                numero = matriz[i][j]
                archivo_texto.write(str(num_alfabeto[numero]))
        archivo_texto.write("\n")
    archivo_texto.close()
    print("¡Partida guardada con éxito!")
    introducir_nuevo_elemento = False

    return introducir_nuevo_elemento

######################
# Programa principal #
######################

main()
"Llamada al programa principal, siendo este la función main"
