#Integrantes:
    # - Agustin Franchini
    # - Nicolas Font
    # - Santino Manoni

#Importacion de librerias
import random
import os

#Cantidad maxima de jugadores permitidos por juego
maximo_jugadores = 10

#Cantidad maxima de cartas que puede llegar a tener una mano en Blackjack
maximo_cartas_mano = 21

def limpiar_consola():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


#-------------------------------------------------------------
# Arreglos de tamaño fijo para el registro de jugadores de cada juego.
# Cada arreglo tiene "maximo_jugadores" lugares reservados desde el inicio.
# Un contador aparte indica cuantos lugares estan realmente ocupados.
#-------------------------------------------------------------

#Mayor o Menor: nombre y ultima racha de cada jugador
mm_nombres = [""] * maximo_jugadores
mm_rachas = [0] * maximo_jugadores
mm_cantidad_registrados = 0

#Numero Secreto: nombre, partidas jugadas, ganadas y perdidas
ns_nombres = [""] * maximo_jugadores
ns_partidas = [0] * maximo_jugadores
ns_ganadas = [0] * maximo_jugadores
ns_perdidas = [0] * maximo_jugadores
ns_cantidad_registrados = 0

#Blackjack: nombre, partidas jugadas y ganadas
bj_nombres = [""] * maximo_jugadores
bj_partidas = [0] * maximo_jugadores
bj_ganadas = [0] * maximo_jugadores
bj_cantidad_registrados = 0

#Par o Impar (dados): nombre, credito actual y cantidad de aciertos
pi_nombres = [""] * maximo_jugadores
pi_creditos = [0] * maximo_jugadores
pi_aciertos = [0] * maximo_jugadores
pi_cantidad_registrados = 0


#-------------------------------------------------------------
#Carteles
#-------------------------------------------------------------
def cartel():
    print("*" * 60)
    print(" BIENVENIDOS A LA CASA DE APUESTAS: 'EL APOSTADOR FELIZ' ")
    print("*" * 60)

def cartel1():
    print("¡Disclaimer!")
    print("*Los juegos de apuestas estan prohibidos para los menores de edad!! y son perjudiciales para la salud*")


#-------------------------------------------------------------
#Menu Principal
#-------------------------------------------------------------
def menu():
    print("\nMENU PRINCIPAL")
    print("¿Qué juego quieres jugar?")
    print("A. Mayor o menor")
    print("B. Numero secreto")
    print("C. Blackjack")
    print("D. Dados - Par e Impar")
    print("E. Reporte")
    print("S. Salir")


#-------------------------------------------------------------
#Funcion generica de busqueda de un jugador dentro de un arreglo de nombres.
#Solo recorre las posiciones realmente ocupadas (cantidad_registrados).
#-------------------------------------------------------------
def buscar_indice(nombres, cantidad_registrados, nombre_buscado):
    #Declaracion de variables:
    #indice_actual: int -> posicion que se va recorriendo del arreglo
    #indice_encontrado: int -> indice donde se encontro el nombre buscado (-1 si no se encontro)
    #ya_se_encontro: bool -> indica si ya se encontro el nombre, para dejar de comparar sin usar break

    indice_encontrado = -1
    ya_se_encontro = False
    for indice_actual in range(cantidad_registrados):
        if not ya_se_encontro:
            if nombres[indice_actual].lower() == nombre_buscado.lower():
                indice_encontrado = indice_actual
                ya_se_encontro = True
    return indice_encontrado


#-------------------------------------------------------------
# Juego 1: Mayor o Menor
#-------------------------------------------------------------
def mayor_menor():
    #Declaracion de variables:
    #nombre: str -> nombre ingresado por el usuario
    #indice_jugador: int -> posicion del jugador dentro de los arreglos mm_nombres / mm_rachas
    #numero_secreto: int -> numero que se muestra en pantalla en cada ronda
    #numero_siguiente: int -> numero generado al azar que se compara contra el actual
    #cont_aciertos: int -> racha de aciertos del jugador en la partida actual
    #bandera: bool -> indica si el jugador sigue en partida o ya perdió
    #intentos: str -> respuesta del jugador ("mayor" o "menor")

    global mm_cantidad_registrados

    print("¡Bienvenido al juego de Mayor o Menor!")
    nombre = input("Ingrese su nombre de usuario: ")
    while nombre == "":
        nombre = input("El nombre no puede estar vacío. Ingrese su nombre de usuario: ")

    indice_jugador = buscar_indice(mm_nombres, mm_cantidad_registrados, nombre)
    if indice_jugador == -1:
        if mm_cantidad_registrados >= maximo_jugadores:
            print("No hay cupos disponibles para nuevos jugadores en este juego.")
            return
        mm_nombres[mm_cantidad_registrados] = nombre
        mm_rachas[mm_cantidad_registrados] = 0
        indice_jugador = mm_cantidad_registrados
        mm_cantidad_registrados += 1
    else:
        print("¡Bienvenido de nuevo,", nombre, "!")

    numero_secreto = random.randint(1, 1000)
    numero_siguiente = random.randint(1, 1000)
    cont_aciertos = 0
    bandera = True

    while bandera:
        print("El número es:", numero_secreto)
        intentos = input("Ingrese si el siguiente numero es mayor o menor: ").lower()

        if intentos == "mayor":
            if numero_secreto < numero_siguiente:
                print(nombre, "¡Correcto! El número secreto es mayor.")
                cont_aciertos += 1
            else:
                print(nombre, "¡Incorrecto! El número secreto es menor. El numero era:", numero_siguiente)
                bandera = False
            numero_secreto = numero_siguiente
            numero_siguiente = random.randint(1, 1000)

        elif intentos == "menor":
            if numero_secreto > numero_siguiente:
                print(nombre, "¡Correcto! El número secreto es menor.")
                cont_aciertos += 1
            else:
                print(nombre, "¡Incorrecto! El número secreto es mayor. El numero era:", numero_siguiente)
                bandera = False
            numero_secreto = numero_siguiente
            numero_siguiente = random.randint(1, 1000)

        else:
            print("Entrada no válida. Por favor, ingrese 'mayor' o 'menor'.")

    print("¡Juego terminado!", nombre, " Has tenido: ", cont_aciertos, "aciertos.")
    mm_rachas[indice_jugador] = cont_aciertos


#-------------------------------------------------------------
# Juego 2: Numero Secreto
#-------------------------------------------------------------
def numero_secreto():
    #Declaracion de variables:
    #nombre_jugador: str -> nombre ingresado por el usuario
    #indice_jugador: int -> posicion del jugador dentro de los arreglos ns_nombres / ns_partidas / ns_ganadas / ns_perdidas
    #numero_a_adivinar: int -> numero secreto generado al azar
    #intentos_realizados: int -> cantidad de intentos que ya uso el jugador
    #intentos_maximos: int -> cantidad maxima de intentos permitidos
    #jugador_acerto: bool -> indica si el jugador adivino el numero
    #numero_ingresado_texto: str -> lo que el jugador escribe por teclado (antes de convertir a int)
    #numero_ingresado: int -> numero que el jugador intenta adivinar, ya convertido a entero

    global ns_cantidad_registrados

    print("¡Bienvenido al juego Numero Secreto!")
    nombre_jugador = input("Ingrese su nombre de usuario: ")
    while nombre_jugador == "":
        nombre_jugador = input("El nombre no puede estar vacío. Ingrese su nombre de usuario: ")

    indice_jugador = buscar_indice(ns_nombres, ns_cantidad_registrados, nombre_jugador)
    if indice_jugador == -1:
        if ns_cantidad_registrados >= maximo_jugadores:
            print("No hay cupos disponibles para nuevos jugadores en este juego.")
            return
        ns_nombres[ns_cantidad_registrados] = nombre_jugador
        ns_partidas[ns_cantidad_registrados] = 0
        ns_ganadas[ns_cantidad_registrados] = 0
        ns_perdidas[ns_cantidad_registrados] = 0
        indice_jugador = ns_cantidad_registrados
        ns_cantidad_registrados += 1
    else:
        print("¡Bienvenido de nuevo,", nombre_jugador, "!")

    numero_a_adivinar = random.randint(1, 100)
    intentos_realizados = 0
    intentos_maximos = 6
    jugador_acerto = False

    while intentos_realizados < intentos_maximos and not jugador_acerto:
        print("Le quedan", intentos_maximos - intentos_realizados, "intentos.")
        numero_ingresado_texto = input("Ingrese un número entre 1 y 100: ")

        while (not numero_ingresado_texto.isdigit()) or int(numero_ingresado_texto) < 1 or int(numero_ingresado_texto) > 100:
            numero_ingresado_texto = input("Error. Ingrese un número entre 1 y 100: ")

        numero_ingresado = int(numero_ingresado_texto)
        intentos_realizados += 1

        if numero_ingresado < numero_a_adivinar:
            print(nombre_jugador, "¡El número secreto es mayor!")
        elif numero_ingresado > numero_a_adivinar:
            print(nombre_jugador, "¡El número secreto es menor!")
        else:
            print(nombre_jugador, "¡Felicidades! has adivinado el número secreto:", numero_a_adivinar, "en", intentos_realizados, "intentos!")
            jugador_acerto = True

    if not jugador_acerto:
        print(nombre_jugador, "¡Lo siento! has agotado tus intentos! El número secreto era:", numero_a_adivinar)

    ns_partidas[indice_jugador] += 1
    if jugador_acerto:
        ns_ganadas[indice_jugador] += 1
    else:
        ns_perdidas[indice_jugador] += 1


#-------------------------------------------------------------
# Juego 3: Blackjack
#-------------------------------------------------------------
def crear_mazo():
    #Declaracion de variables:
    #palos: arr[str] -> los 4 palos de la baraja
    #valores: arr[str] -> los 13 valores posibles de cada carta
    #cantidad_cartas: int -> cantidad total de cartas del mazo (52)
    #mazo: mat[str] -> matriz de 52 filas x 2 columnas; cada fila es una carta [valor, palo]
    #indice_carta: int -> posicion que se va llenando dentro del mazo
    #indice_palo: int -> palo que se esta recorriendo
    #indice_valor: int -> valor que se esta recorriendo
    #indice_actual: int -> posicion actual durante el mezclado
    #indice_aleatorio: int -> posicion aleatoria con la que se intercambia durante el mezclado

    palos = [""] * 4
    palos[0] = "Corazones"
    palos[1] = "Diamantes"
    palos[2] = "Treboles"
    palos[3] = "Picas"

    valores = [""] * 13
    valores[0] = "2"
    valores[1] = "3"
    valores[2] = "4"
    valores[3] = "5"
    valores[4] = "6"
    valores[5] = "7"
    valores[6] = "8"
    valores[7] = "9"
    valores[8] = "10"
    valores[9] = "J"
    valores[10] = "Q"
    valores[11] = "K"
    valores[12] = "A"

    cantidad_cartas = len(palos) * len(valores)

    mazo = [""] * cantidad_cartas

    indice_carta = 0
    for indice_palo in range(len(palos)):
        for indice_valor in range(len(valores)):
            mazo[indice_carta] = [valores[indice_valor], palos[indice_palo]]
            indice_carta += 1

    #Mezclado manual del mazo (intercambio de filas completas al azar)
    for indice_actual in range(cantidad_cartas - 1, 0, -1):
        indice_aleatorio = random.randint(0, indice_actual)
        mazo[indice_actual], mazo[indice_aleatorio] = mazo[indice_aleatorio], mazo[indice_actual]

    return mazo

def valor_carta(valor_de_la_carta):
    if valor_de_la_carta == "J" or valor_de_la_carta == "Q" or valor_de_la_carta == "K":
        return 10
    elif valor_de_la_carta == "A":
        return 11
    else:
        return int(valor_de_la_carta)

def calcular_puntaje(valores_mano, cantidad_cartas_mano):
    #Declaracion de variables:
    #puntaje_total: int -> suma de los valores de las cartas de la mano
    #cantidad_ases: int -> cantidad de ases presentes en la mano
    #indice_carta: int -> posicion que se esta recorriendo dentro de la mano

    puntaje_total = 0
    cantidad_ases = 0
    for indice_carta in range(cantidad_cartas_mano):
        puntaje_total += valor_carta(valores_mano[indice_carta])
        if valores_mano[indice_carta] == "A":
            cantidad_ases += 1
    while puntaje_total > 21 and cantidad_ases > 0:
        puntaje_total -= 10
        cantidad_ases -= 1
    return puntaje_total

def mostrar_mano(valores_mano, palos_mano, cantidad_cartas_mano, puntaje, nombre_quien):
    #Declaracion de variables:
    #texto_cartas: str -> texto armado con todas las cartas de la mano para mostrar por pantalla
    #indice_carta: int -> posicion que se esta recorriendo dentro de la mano

    texto_cartas = ""
    for indice_carta in range(cantidad_cartas_mano):
        texto_cartas += valores_mano[indice_carta] + " de " + palos_mano[indice_carta] + " | "
    print(nombre_quien, "tiene:", texto_cartas, "-> Total:", puntaje)

def blackjack():
    #Declaracion de variables:
    #nombre_jugador: str -> nombre ingresado por el usuario
    #indice_jugador: int -> posicion del jugador dentro de los arreglos bj_nombres / bj_partidas / bj_ganadas
    #quiere_jugar_de_nuevo: bool -> indica si el jugador quiere iniciar otra partida
    #mazo: mat[str] -> matriz de 52 cartas ya mezclada (cada fila es [valor, palo])
    #proxima_carta: int -> puntero a la siguiente carta sin repartir dentro del mazo
    #cartas_jugador_valores, cartas_jugador_palos: arr[str] -> cartas que tiene el jugador en la mano
    #cantidad_cartas_jugador: int -> cantidad de cartas que tiene el jugador en la mano
    #cartas_banca_valores, cartas_banca_palos: arr[str] -> cartas que tiene la banca en la mano
    #cantidad_cartas_banca: int -> cantidad de cartas que tiene la banca en la mano
    #puntaje_jugador: int -> puntaje actual del jugador
    #puntaje_banca: int -> puntaje actual de la banca
    #jugador_se_paso: bool -> indica si el jugador supero los 21 puntos
    #es_turno_jugador: bool -> indica si todavia es el turno del jugador
    #decision_jugador: str -> decision del jugador ("pedir" o "plantarse")
    #respuesta_usuario: str -> respuesta del jugador ante "¿jugar otra partida?"

    global bj_cantidad_registrados

    print("¡Bienvenido al Blackjack!")
    nombre_jugador = input("Ingrese su nombre de usuario: ")
    while nombre_jugador == "":
        nombre_jugador = input("El nombre no puede estar vacío. Ingrese su nombre de usuario: ")

    indice_jugador = buscar_indice(bj_nombres, bj_cantidad_registrados, nombre_jugador)
    if indice_jugador == -1:
        if bj_cantidad_registrados >= maximo_jugadores:
            print("No hay cupos disponibles para nuevos jugadores en este juego.")
            return
        bj_nombres[bj_cantidad_registrados] = nombre_jugador
        bj_partidas[bj_cantidad_registrados] = 0
        bj_ganadas[bj_cantidad_registrados] = 0
        indice_jugador = bj_cantidad_registrados
        bj_cantidad_registrados += 1
    else:
        print("¡Bienvenido de nuevo,", nombre_jugador, "!")

    quiere_jugar_de_nuevo = True
    while quiere_jugar_de_nuevo:
        mazo = crear_mazo()
        proxima_carta = 0

        cartas_jugador_valores = [""] * maximo_cartas_mano
        cartas_jugador_palos = [""] * maximo_cartas_mano
        cantidad_cartas_jugador = 0

        cartas_banca_valores = [""] * maximo_cartas_mano
        cartas_banca_palos = [""] * maximo_cartas_mano
        cantidad_cartas_banca = 0

        #Reparto inicial: 2 cartas para el jugador y 2 para la banca
        cartas_jugador_valores[0] = mazo[proxima_carta][0]
        cartas_jugador_palos[0] = mazo[proxima_carta][1]
        proxima_carta += 1
        cartas_jugador_valores[1] = mazo[proxima_carta][0]
        cartas_jugador_palos[1] = mazo[proxima_carta][1]
        proxima_carta += 1
        cantidad_cartas_jugador = 2

        cartas_banca_valores[0] = mazo[proxima_carta][0]
        cartas_banca_palos[0] = mazo[proxima_carta][1]
        proxima_carta += 1
        cartas_banca_valores[1] = mazo[proxima_carta][0]
        cartas_banca_palos[1] = mazo[proxima_carta][1]
        proxima_carta += 1
        cantidad_cartas_banca = 2

        puntaje_jugador = calcular_puntaje(cartas_jugador_valores, cantidad_cartas_jugador)
        puntaje_banca = calcular_puntaje(cartas_banca_valores, cantidad_cartas_banca)

        print("\nLa banca muestra:", cartas_banca_valores[0], "de", cartas_banca_palos[0], "y una carta oculta")
        mostrar_mano(cartas_jugador_valores, cartas_jugador_palos, cantidad_cartas_jugador, puntaje_jugador, nombre_jugador)

        jugador_se_paso = False
        es_turno_jugador = True
        while es_turno_jugador:
            if puntaje_jugador == 21:
                print("¡Blackjack! Pasa el turno a la banca automáticamente.")
                es_turno_jugador = False
            else:
                decision_jugador = input("¿Quiere 'Pedir' o 'Plantarse'? ").lower()
                if decision_jugador == "pedir":
                    cartas_jugador_valores[cantidad_cartas_jugador] = mazo[proxima_carta][0]
                    cartas_jugador_palos[cantidad_cartas_jugador] = mazo[proxima_carta][1]
                    cantidad_cartas_jugador += 1
                    proxima_carta += 1
                    puntaje_jugador = calcular_puntaje(cartas_jugador_valores, cantidad_cartas_jugador)
                    mostrar_mano(cartas_jugador_valores, cartas_jugador_palos, cantidad_cartas_jugador, puntaje_jugador, nombre_jugador)
                    if puntaje_jugador > 21:
                        jugador_se_paso = True
                        es_turno_jugador = False
                elif decision_jugador == "plantarse":
                    es_turno_jugador = False
                else:
                    print("Entrada no válida. Por favor, ingrese 'Pedir' o 'Plantarse'.")

        if jugador_se_paso:
            print(nombre_jugador, "se pasó de 21. ¡Pierde la partida!")
        else:
            print("\nTurno de la banca...")
            mostrar_mano(cartas_banca_valores, cartas_banca_palos, cantidad_cartas_banca, puntaje_banca, "Banca")
            while puntaje_banca < 17:
                cartas_banca_valores[cantidad_cartas_banca] = mazo[proxima_carta][0]
                cartas_banca_palos[cantidad_cartas_banca] = mazo[proxima_carta][1]
                cantidad_cartas_banca += 1
                proxima_carta += 1
                puntaje_banca = calcular_puntaje(cartas_banca_valores, cantidad_cartas_banca)
                print("La banca pide carta.")
                mostrar_mano(cartas_banca_valores, cartas_banca_palos, cantidad_cartas_banca, puntaje_banca, "Banca")

            if puntaje_banca > 21:
                print("¡La banca se pasó de 21!", nombre_jugador, "¡gana la partida!")
                bj_ganadas[indice_jugador] += 1
            elif puntaje_banca > puntaje_jugador:
                print("La banca gana la partida.")
            elif puntaje_banca < puntaje_jugador:
                print(nombre_jugador, "¡gana la partida!")
                bj_ganadas[indice_jugador] += 1
            else:
                print("¡Empate!")

        bj_partidas[indice_jugador] += 1

        respuesta_usuario = input("¿Quiere jugar otra partida? (si/no): ").lower()
        while respuesta_usuario != "si" and respuesta_usuario != "no":
            respuesta_usuario = input("Entrada no válida. ¿Quiere jugar otra partida? (si/no): ").lower()
        quiere_jugar_de_nuevo = (respuesta_usuario == "si")


#-------------------------------------------------------------
# Juego 4: Dados - Par e Impar (con credito)
#-------------------------------------------------------------
def dados_par_impar():
    #Declaracion de variables:
    #nombre_jugador: str -> nombre ingresado por el usuario
    #indice_jugador: int -> posicion del jugador dentro de los arreglos pi_nombres / pi_creditos / pi_aciertos
    #juego_activo: bool -> indica si el jugador sigue jugando
    #apuesta_texto: str -> monto apostado ingresado por teclado (antes de convertir a int)
    #monto_apuesta: int -> monto apostado ya convertido a entero
    #dado1: int -> resultado del primer dado
    #dado2: int -> resultado del segundo dado
    #suma_dados: int -> suma de ambos dados
    #respuesta_par_impar: str -> respuesta del jugador ("par" o "impar")
    #resultado_es_par: bool -> indica si la suma de los dados dio par
    #respuesta_usuario: str -> respuesta del jugador ante "¿seguir jugando?"

    global pi_cantidad_registrados

    print("¡Bienvenido al juego de Par o Impar!")
    nombre_jugador = input("Ingrese su nombre de usuario: ")
    while nombre_jugador == "":
        nombre_jugador = input("El nombre no puede estar vacío. Ingrese su nombre de usuario: ")

    indice_jugador = buscar_indice(pi_nombres, pi_cantidad_registrados, nombre_jugador)
    if indice_jugador == -1:
        if pi_cantidad_registrados >= maximo_jugadores:
            print("No hay cupos disponibles para nuevos jugadores en este juego.")
            return
        pi_nombres[pi_cantidad_registrados] = nombre_jugador
        pi_creditos[pi_cantidad_registrados] = 1000
        pi_aciertos[pi_cantidad_registrados] = 0
        indice_jugador = pi_cantidad_registrados
        pi_cantidad_registrados += 1
    else:
        print("¡Bienvenido de nuevo,", nombre_jugador, "!")

    if pi_creditos[indice_jugador] <= 0:
        print(nombre_jugador, ", no te queda credito disponible para jugar.")
        return

    juego_activo = True
    while juego_activo and pi_creditos[indice_jugador] > 0:
        print("Crédito actual de", nombre_jugador, ":", pi_creditos[indice_jugador])
        apuesta_texto = input("Ingrese cuanto quiere apostar: ")
        while (not apuesta_texto.isdigit()) or int(apuesta_texto) <= 0 or int(apuesta_texto) > pi_creditos[indice_jugador]:
            apuesta_texto = input("Apuesta inválida. Ingrese un monto entre 1 y " + str(pi_creditos[indice_jugador]) + ": ")
        monto_apuesta = int(apuesta_texto)

        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        suma_dados = dado1 + dado2

        respuesta_par_impar = input(nombre_jugador + ", ingrese si el resultado de la suma de los dados es par o impar: ").lower()
        while respuesta_par_impar != "par" and respuesta_par_impar != "impar":
            respuesta_par_impar = input("Entrada no válida. Ingrese 'par' o 'impar': ").lower()

        resultado_es_par = (suma_dados % 2 == 0)
        if (respuesta_par_impar == "par" and resultado_es_par) or (respuesta_par_impar == "impar" and not resultado_es_par):
            print(nombre_jugador, "¡Correcto! El resultado fue:", suma_dados)
            pi_creditos[indice_jugador] += monto_apuesta
            pi_aciertos[indice_jugador] += 1
        else:
            print(nombre_jugador, "¡Incorrecto! El resultado fue:", suma_dados)
            pi_creditos[indice_jugador] -= monto_apuesta

        if pi_creditos[indice_jugador] <= 0:
            print(nombre_jugador, "se quedó sin crédito. ¡Juego terminado!")
            juego_activo = False
        else:
            respuesta_usuario = input("¿Quiere seguir jugando? (si/no): ").lower()
            while respuesta_usuario != "si" and respuesta_usuario != "no":
                respuesta_usuario = input("Entrada no válida. ¿Quiere seguir jugando? (si/no): ").lower()
            juego_activo = (respuesta_usuario == "si")

    print(nombre_jugador, "finalizó el juego con un crédito de", pi_creditos[indice_jugador], "y", pi_aciertos[indice_jugador], "aciertos totales.")


#-------------------------------------------------------------
# Juego 5: Reporte (submenu)
#-------------------------------------------------------------
def mostrar_ranking(nombres, valores, cantidad_registrados, etiqueta):
    #Declaracion de variables:
    #nombres_ordenados: arr[str] -> copia de los nombres realmente registrados, se ordena sin modificar el original
    #valores_ordenados: arr[int] -> copia de los valores realmente registrados, se ordena sin modificar el original
    #indice_copia: int -> posicion usada para copiar manualmente los datos
    #indice_i: int -> contador externo del ordenamiento burbuja
    #indice_j: int -> contador interno del ordenamiento burbuja

    if cantidad_registrados == 0:
        print("No hay jugadores registrados en este juego.")
        return

    #Copiamos manualmente, elemento por elemento, para no modificar los arreglos originales
    nombres_ordenados = [""] * cantidad_registrados
    valores_ordenados = [0] * cantidad_registrados
    for indice_copia in range(cantidad_registrados):
        nombres_ordenados[indice_copia] = nombres[indice_copia]
        valores_ordenados[indice_copia] = valores[indice_copia]

    #Ordenamiento burbuja de mayor a menor
    for indice_i in range(cantidad_registrados):
        for indice_j in range(0, cantidad_registrados - indice_i - 1):
            if valores_ordenados[indice_j] < valores_ordenados[indice_j + 1]:
                valores_ordenados[indice_j], valores_ordenados[indice_j + 1] = valores_ordenados[indice_j + 1], valores_ordenados[indice_j]
                nombres_ordenados[indice_j], nombres_ordenados[indice_j + 1] = nombres_ordenados[indice_j + 1], nombres_ordenados[indice_j]

    for indice_i in range(cantidad_registrados):
        print(nombres_ordenados[indice_i], "-", valores_ordenados[indice_i], etiqueta)

def reporte_ranking_ganadores():
    print("\n--- Ranking Número Secreto (partidas ganadas) ---")
    mostrar_ranking(ns_nombres, ns_ganadas, ns_cantidad_registrados, "partidas ganadas")

    print("\n--- Ranking Blackjack (partidas ganadas) ---")
    mostrar_ranking(bj_nombres, bj_ganadas, bj_cantidad_registrados, "partidas ganadas")

    print("\n--- Ranking Par o Impar (aciertos) ---")
    mostrar_ranking(pi_nombres, pi_aciertos, pi_cantidad_registrados, "aciertos")

def reporte_juegos_jugador():
    #Declaracion de variables:
    #nombre_jugador: str -> nombre del jugador a consultar
    #jugador_encontrado: bool -> indica si el jugador aparecio en al menos un juego
    #indice_jugador: int -> posicion del jugador dentro del arreglo de nombres de cada juego

    nombre_jugador = input("Ingrese el nombre del jugador a consultar: ")
    jugador_encontrado = False

    indice_jugador = buscar_indice(mm_nombres, mm_cantidad_registrados, nombre_jugador)
    if indice_jugador != -1:
        print(nombre_jugador, "jugó a Mayor o Menor. Racha:", mm_rachas[indice_jugador], "puntos.")
        jugador_encontrado = True

    indice_jugador = buscar_indice(ns_nombres, ns_cantidad_registrados, nombre_jugador)
    if indice_jugador != -1:
        print(nombre_jugador, "jugó a Número Secreto. Partidas ganadas:", ns_ganadas[indice_jugador], "puntos.")
        jugador_encontrado = True

    indice_jugador = buscar_indice(bj_nombres, bj_cantidad_registrados, nombre_jugador)
    if indice_jugador != -1:
        print(nombre_jugador, "jugó a Blackjack. Partidas ganadas:", bj_ganadas[indice_jugador], "puntos.")
        jugador_encontrado = True

    indice_jugador = buscar_indice(pi_nombres, pi_cantidad_registrados, nombre_jugador)
    if indice_jugador != -1:
        print(nombre_jugador, "jugó a Par o Impar. Aciertos:", pi_aciertos[indice_jugador], "puntos. Crédito actual:", pi_creditos[indice_jugador])
        jugador_encontrado = True

    if not jugador_encontrado:
        print("El jugador", nombre_jugador, "no registra partidas jugadas.")

def reporte_credito():
    #Declaracion de variables:
    #nombres_ordenados: arr[str] -> copia de los nombres realmente registrados, se ordena sin modificar el original
    #creditos_ordenados: arr[int] -> copia de los creditos realmente registrados, se ordena sin modificar el original
    #indice_copia: int -> posicion usada para copiar manualmente los datos
    #indice_i: int -> contador externo del ordenamiento burbuja
    #indice_j: int -> contador interno del ordenamiento burbuja

    if pi_cantidad_registrados == 0:
        print("No hay jugadores registrados en Par o Impar.")
        return

    nombres_ordenados = [""] * pi_cantidad_registrados
    creditos_ordenados = [0] * pi_cantidad_registrados
    for indice_copia in range(pi_cantidad_registrados):
        nombres_ordenados[indice_copia] = pi_nombres[indice_copia]
        creditos_ordenados[indice_copia] = pi_creditos[indice_copia]

    #Ordenamiento burbuja de menor a mayor
    for indice_i in range(pi_cantidad_registrados):
        for indice_j in range(0, pi_cantidad_registrados - indice_i - 1):
            if creditos_ordenados[indice_j] > creditos_ordenados[indice_j + 1]:
                creditos_ordenados[indice_j], creditos_ordenados[indice_j + 1] = creditos_ordenados[indice_j + 1], creditos_ordenados[indice_j]
                nombres_ordenados[indice_j], nombres_ordenados[indice_j + 1] = nombres_ordenados[indice_j + 1], nombres_ordenados[indice_j]

    for indice_i in range(pi_cantidad_registrados):
        print(nombres_ordenados[indice_i], "- Crédito:", creditos_ordenados[indice_i])

def reporte_racha():
    #Declaracion de variables:
    #nombre_jugador: str -> nombre del jugador a consultar
    #indice_jugador: int -> posicion del jugador dentro del arreglo mm_nombres

    nombre_jugador = input("Ingrese el nombre del jugador: ")
    indice_jugador = buscar_indice(mm_nombres, mm_cantidad_registrados, nombre_jugador)
    if indice_jugador == -1:
        print("El jugador", nombre_jugador, "no registra partidas de Mayor o Menor.")
    else:
        print(nombre_jugador, "tiene una racha de", mm_rachas[indice_jugador], "en Mayor o Menor.")

def menu_reporte():
    print("\nREPORTE")
    print("A. Lista de jugadores ordenados por cantidad de veces que ganaron cada juego (excepto Mayor/Menor)")
    print("B. Juegos jugados por un jugador")
    print("C. Listado de jugadores de Par-Impar ordenado por crédito (menor a mayor)")
    print("D. Racha de un jugador en Mayor/Menor")
    print("E. Volver al menú principal")

def reporte():
    #Declaracion de variables:
    #opc: str -> opcion del submenu de reporte ingresada por el usuario

    opc = ""
    while opc != "E":
        menu_reporte()
        opc = input("Ingrese su opción: ").upper()
        while opc != "A" and opc != "B" and opc != "C" and opc != "D" and opc != "E":
            opc = input("Ingreso invalido - reintente: ").upper()

        limpiar_consola()

        match opc:
            case "A":
                reporte_ranking_ganadores()
            case "B":
                reporte_juegos_jugador()
            case "C":
                reporte_credito()
            case "D":
                reporte_racha()
            case "E":
                pass


#-------------------------------------------------------------
#Programa Principal
#-------------------------------------------------------------
#Declaracion de variables:
#opc: str -> opcion del menu principal ingresada por el usuario

cartel()
cartel1()
input("Presione Enter para continuar...")

opc = ""
while opc != "S":
    menu()
    opc = input("Ingrese su opcion: ").upper()
    while opc != "A" and opc != "B" and opc != "C" and opc != "D" and opc != "E" and opc != "S":
        opc = input("Ingreso invalido - reintente: ").upper()

    limpiar_consola()

    match opc:
        case "A":
            mayor_menor()
        case "B":
            numero_secreto()
        case "C":
            blackjack()
        case "D":
            dados_par_impar()
        case "E":
            reporte()
        case "S":
            print("Gracias por jugar, no apueste, juega por diversión")
            input("Presione Enter para continuar...")
