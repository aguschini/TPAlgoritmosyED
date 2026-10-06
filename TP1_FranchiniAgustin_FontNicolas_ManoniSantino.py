#Integrantes:
    # - Agustin Franchini
    # - Nicolas Font
    # - Santino Manoni

#Importacion de librerias
import getpass
import pickle
import random
import os

#Variables globales: cantidad maxima de jugadores permitidos por juego y cantidad maxima de cartas que puede llegar a tener una mano en Blackjack
CLAVE_ADMIN = "admin123"
maximo_jugadores = 10
maximo_cartas_mano = 21

def limpiar_consola():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


#-------------------------------------------------------------
# Clases
#-------------------------------------------------------------
class Categorias:
    def __init__(self):
        self.nrocategoria = 0
        self.nombrecategoria = " "
        self.pregunta = " "
        self.estado = " " #A/I

class Opciones:
    def __init__(self):
        self.nrocategoria = 0
        self.nroopcion = 0
        self.objeto = " "
        self.valor = 0

class Jugadores:
    def __init__(self):
        self.nombre = " "
        self.creditos = 0
        self.juegos = [[0] * 4 for i in range(2)]
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
    print("A. Juego del menor-mayor")
    print("B. Adivinar el número secreto")
    print("C. Blackjack")
    print("D. Par o impar")
    print("E. Reporte")
    print("F. Administración de Juegos")
    print("G. Salir del programa")


#-------------------------------------------------------------
#Funcion de busqueda de un jugador dentro de un arreglo de nombres.
#-------------------------------------------------------------
def tamanio_archivo(AL):
    AL.seek(0, 2)
    return AL.tell()

def buscar_jugador(ALJ, nombre):
    pos_encontrada = -1
    t = tamanio_archivo(ALJ)
    ALJ.seek(0)
    while ALJ.tell() < t and pos_encontrada == -1:
        pos_actual = ALJ.tell()
        RJ = pickle.load(ALJ)
        if RJ.nombre.strip().lower() == nombre.strip().lower():
            pos_encontrada = pos_actual
    return pos_encontrada

def alta_jugador(ALJ, nombre):
    RJ.nombre = nombre.strip().ljust(30)
    RJ.creditos = 10000.0
    pos = tamanio_archivo(ALJ)
    ALJ.seek(pos)
    pickle.dump(RJ, ALJ)
    ALJ.flush()
    return pos

def registrar_resultado(ALJ, pos, juego, gano, monto):
    # juego: 0 mayor/menor, 1 num. secreto, 2 blackjack, 3 par/impar
    # fila 0 = ganadas, fila 1 = perdidas
    # monto: créditos a sumar (positivo) o restar (negativo); 0 si no hay apuesta
    ALJ.seek(pos)
    RJ = pickle.load(ALJ)
    if gano:
        RJ.juegos[0][juego] += 1
    else:
        RJ.juegos[1][juego] += 1
    RJ.creditos += monto
    ALJ.seek(pos)
    pickle.dump(RJ, ALJ)
    ALJ.flush()

#-------------------------------------------------------------
# Juego 1: Mayor o Menor
#-------------------------------------------------------------
def mostrar_categorias_activas(ALC):
    t = tamanio_archivo(ALC)
    cantidad = 0
    ALC.seek(0)
    while ALC.tell() < t:
        RC = pickle.load(ALC)
        if RC.estado == "A":
            print(RC.nrocategoria, "-", RC.nombrecategoria.strip())
            cantidad += 1
    return cantidad

def buscar_categoria_activa(ALC, nro):
    pos_encontrada = -1
    t = tamanio_archivo(ALC)
    ALC.seek(0)
    while ALC.tell() < t and pos_encontrada == -1:
        pos_actual = ALC.tell()
        RC = pickle.load(ALC)
        if RC.nrocategoria == nro and RC.estado == "A":
            pos_encontrada = pos_actual
    return pos_encontrada

def leer_pregunta(ALC, pos):
    ALC.seek(pos)
    RC = pickle.load(ALC)
    return RC.pregunta.strip()

def contar_opciones(ALO, nro_categoria):
    t = tamanio_archivo(ALO)
    cantidad = 0
    ALO.seek(0)
    while ALO.tell() < t:
        RO = pickle.load(ALO)
        if RO.nrocategoria == nro_categoria:
            cantidad += 1
    return cantidad

def buscar_opcion_k(ALO, nro_categoria, k):
    # devuelve la posición de la k-ésima opción (1, 2, 3...) de esa categoría
    pos_encontrada = -1
    contador = 0
    t = tamanio_archivo(ALO)
    ALO.seek(0)
    while ALO.tell() < t and pos_encontrada == -1:
        pos_actual = ALO.tell()
        RO = pickle.load(ALO)
        if RO.nrocategoria == nro_categoria:
            contador += 1
            if contador == k:
                pos_encontrada = pos_actual
    return pos_encontrada

def leer_objeto(ALO, pos):
    ALO.seek(pos)
    RO = pickle.load(ALO)
    return RO.objeto.strip()

def leer_valor(ALO, pos):
    ALO.seek(pos)
    RO = pickle.load(ALO)
    return RO.valor


def mayor_menor(ALC, ALO, ALJ):
    """ declarative de Variables utilizadas
    nombre_jugador, apuesta_texto, categoria_texto, pregunta, objeto_a, objeto_b, respuesta: string
    pos_jugador, monto_apuesta, cantidad_activas, nro_categoria, pos_categoria, cantidad_opciones: int
    k_a, k_b, pos_a, pos_b, valor_a, valor_b, aciertos, ronda: int
    rondas_totales, minimo_aciertos, minimo_opciones: int
    creditos_actuales: float
    categoria_valida, cancelado, acerto: bool
    """

    rondas_totales = 6
    minimo_aciertos = 4
    minimo_opciones = 6

    print("¡Bienvenido al Juego del Menor-Mayor!")
    nombre_jugador = input("Ingrese su nombre: ")
    while nombre_jugador.strip() == "":
        nombre_jugador = input("El nombre no puede estar vacío. Ingrese su nombre: ")
    nombre_jugador = nombre_jugador.strip()

    pos_jugador = buscar_jugador(ALJ, nombre_jugador)
    if pos_jugador == -1:
        pos_jugador = alta_jugador(ALJ, nombre_jugador)
        print("Jugador nuevo registrado con 10000 créditos.")
    else:
        print("¡Bienvenido de nuevo,", nombre_jugador, "!")

    creditos_actuales = leer_creditos(ALJ, pos_jugador)

    if creditos_actuales <= 0:
        print(nombre_jugador, ", no te queda crédito disponible para jugar.")
    else:
        # --- Apuesta ---
        print("Crédito actual de", nombre_jugador, ":", creditos_actuales)
        apuesta_texto = input("¿Cuántos créditos quiere apostar? ")
        while (not apuesta_texto.isdigit()) or int(apuesta_texto) <= 0 or int(apuesta_texto) > creditos_actuales:
            apuesta_texto = input("Apuesta inválida. Ingrese un monto entre 1 y " + str(int(creditos_actuales)) + ": ")
        monto_apuesta = int(apuesta_texto)

        # --- Elección de categoría ---
        print("\nCategorías disponibles:")
        cantidad_activas = mostrar_categorias_activas(ALC)

        if cantidad_activas == 0:
            print("No hay categorías activas. Pida al administrador que cargue categorías.")
        else:
            categoria_valida = False
            cancelado = False
            nro_categoria = 0
            pos_categoria = -1
            cantidad_opciones = 0

            categoria_texto = input("Elija el número de categoría (0 para volver): ")
            while not categoria_valida and not cancelado:
                if not categoria_texto.isdigit():
                    print("Entrada no válida.")
                elif int(categoria_texto) == 0:
                    cancelado = True
                else:
                    nro_categoria = int(categoria_texto)
                    pos_categoria = buscar_categoria_activa(ALC, nro_categoria)
                    if pos_categoria == -1:
                        print("La categoría no existe o no está activa.")
                    else:
                        cantidad_opciones = contar_opciones(ALO, nro_categoria)
                        if cantidad_opciones < minimo_opciones:
                            print("Esa categoría no tiene suficientes opciones para jugar.")
                        else:
                            categoria_valida = True
                if not categoria_valida and not cancelado:
                    categoria_texto = input("Elija otra categoría (0 para volver): ")

            # --- Partida: 6 rondas ---
            if categoria_valida:
                pregunta = leer_pregunta(ALC, pos_categoria)
                aciertos = 0

                k_a = random.randint(1, cantidad_opciones)
                k_b = random.randint(1, cantidad_opciones)
                while k_b == k_a:
                    k_b = random.randint(1, cantidad_opciones)

                for ronda in range(1, rondas_totales + 1):
                    pos_a = buscar_opcion_k(ALO, nro_categoria, k_a)
                    pos_b = buscar_opcion_k(ALO, nro_categoria, k_b)
                    objeto_a = leer_objeto(ALO, pos_a)
                    objeto_b = leer_objeto(ALO, pos_b)
                    valor_a = leer_valor(ALO, pos_a)
                    valor_b = leer_valor(ALO, pos_b)

                    print("\n--- Ronda", ronda, "de", rondas_totales, "---")
                    print(pregunta)
                    print("1.", objeto_a, "/ 2.", objeto_b)
                    respuesta = input("Su respuesta (1 o 2): ")
                    while respuesta != "1" and respuesta != "2":
                        respuesta = input("Entrada no válida. Ingrese 1 o 2: ")

                    acerto = (respuesta == "1" and valor_a >= valor_b) or (respuesta == "2" and valor_b >= valor_a)
                    if acerto:
                        print("¡Correcto! Suma 1 punto.")
                        aciertos += 1
                    else:
                        print("Incorrecto.")
                    print(objeto_a, valor_a, "/", objeto_b, valor_b)

                    # La opción correcta pasa a la ronda siguiente
                    if valor_b > valor_a or (valor_a == valor_b and respuesta == "2"):
                        k_a = k_b
                    k_b = random.randint(1, cantidad_opciones)
                    while k_b == k_a:
                        k_b = random.randint(1, cantidad_opciones)

                    if ronda < rondas_totales:
                        input("Presione Enter para continuar...")

                # --- Resultado ---
                print("\nAciertos:", aciertos, "de", rondas_totales)
                if aciertos >= minimo_aciertos:
                    print("¡GANASTE! Ganás", monto_apuesta, "créditos.")
                    registrar_resultado(ALJ, pos_jugador, 0, True, monto_apuesta)
                else:
                    print("Perdiste. Perdés", monto_apuesta, "créditos.")
                    registrar_resultado(ALJ, pos_jugador, 0, False, -monto_apuesta)
                print("Crédito actual:", leer_creditos(ALJ, pos_jugador))
#-------------------------------------------------------------
# Juego 2: Numero Secreto
#-------------------------------------------------------------
def numero_secreto(ALJ):
    """ declarative de Variables utilizadas
    nombre_jugador, numero_ingresado_texto: string
    indice_jugador, numero_a_adivinar, intentos_realizados, intentos_maximos, numero_ingresado: int
    jugador_acerto: bool
    """

    print("¡Bienvenido al juego Numero Secreto!")
    nombre_jugador = input("Ingrese su nombre: ")
    pos_jugador = buscar_jugador(ALJ, nombre_jugador)
    if pos_jugador == -1:
        pos_jugador = alta_jugador(ALJ, nombre_jugador)
    else:
        print("¡Bienvenido de nuevo,", nombre_jugador, "!")
    

    numero_a_adivinar = random.randint(1, 100)
    intentos_realizados = 0
    intentos_maximos = 5
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

    registrar_resultado(ALJ, pos_jugador, 1, jugador_acerto, 0)


#-------------------------------------------------------------
# Juego 3: Blackjack
#-------------------------------------------------------------
def crear_mazo(mazo):
    """ declarative de Variables utilizadas
    palos, valores: arr[string]
    mazo: mat[string] (52 x 2, recibido por parámetro)
    cantidad_cartas, indice_carta, indice_palo, indice_valor, indice_actual, indice_aleatorio: int
    carta_auxiliar_valor, carta_auxiliar_palo: string
    """

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

    indice_carta = 0
    for indice_palo in range(len(palos)):
        for indice_valor in range(len(valores)):
            mazo[indice_carta][0] = valores[indice_valor]
            mazo[indice_carta][1] = palos[indice_palo]
            indice_carta += 1

    # Mezcla (Fisher-Yates)
    for indice_actual in range(cantidad_cartas - 1, 0, -1):
        indice_aleatorio = random.randint(0, indice_actual)
        carta_auxiliar_valor = mazo[indice_actual][0]
        carta_auxiliar_palo = mazo[indice_actual][1]
        mazo[indice_actual][0] = mazo[indice_aleatorio][0]
        mazo[indice_actual][1] = mazo[indice_aleatorio][1]
        mazo[indice_aleatorio][0] = carta_auxiliar_valor
        mazo[indice_aleatorio][1] = carta_auxiliar_palo

def valor_carta(valor_de_la_carta):
    if valor_de_la_carta == "J" or valor_de_la_carta == "Q" or valor_de_la_carta == "K":
        return 10
    elif valor_de_la_carta == "A":
        return 11
    else:
        return int(valor_de_la_carta)

def calcular_puntaje(valores_mano, cantidad_cartas_mano):
    """ declarative de Variables utilizadas
    puntaje_total, cantidad_ases, indice_carta: int
    """

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
    """ declarative de Variables utilizadas
    texto_cartas: string
    indice_carta: int
    """

    texto_cartas = ""
    for indice_carta in range(cantidad_cartas_mano):
        texto_cartas += valores_mano[indice_carta] + " de " + palos_mano[indice_carta] + " | "
    print(nombre_quien, "tiene:", texto_cartas, "-> Total:", puntaje)

def blackjack(ALJ):
    """ declarative de Variables utilizadas
    nombre_jugador, decision_jugador, respuesta_usuario: string
    pos_jugador, proxima_carta, cantidad_cartas_jugador, cantidad_cartas_banca, puntaje_jugador, puntaje_banca, puntaje_banca_visible: int
    quiere_jugar_de_nuevo, jugador_se_paso, es_turno_jugador: bool
    mazo: mat[string]
    cartas_jugador_valores, cartas_jugador_palos, cartas_banca_valores, cartas_banca_palos: arr[string]
    """

    print("¡Bienvenido al Blackjack!")
    nombre_jugador = input("Ingrese su nombre: ")
    while nombre_jugador.strip() == "":
        nombre_jugador = input("El nombre no puede estar vacío. Ingrese su nombre: ")
    nombre_jugador = nombre_jugador.strip()

    pos_jugador = buscar_jugador(ALJ, nombre_jugador)
    if pos_jugador == -1:
        pos_jugador = alta_jugador(ALJ, nombre_jugador)
        print("Jugador nuevo registrado con 10000 créditos.")
    else:
        print("¡Bienvenido de nuevo,", nombre_jugador, "!")

    mazo = [["", ""] for i in range(52)]

    
    quiere_jugar_de_nuevo = True
    while quiere_jugar_de_nuevo:
        crear_mazo(mazo)
        proxima_carta = 0

        cartas_jugador_valores = [""] * maximo_cartas_mano
        cartas_jugador_palos = [""] * maximo_cartas_mano
        cantidad_cartas_jugador = 0

        cartas_banca_valores = [""] * maximo_cartas_mano
        cartas_banca_palos = [""] * maximo_cartas_mano
        cantidad_cartas_banca = 0

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

        # Se muestra solo UNA carta de la banca
        puntaje_banca_visible = calcular_puntaje(cartas_banca_valores, 1)
        print("\nLa banca muestra:")
        mostrar_mano(cartas_banca_valores, cartas_banca_palos, 1, puntaje_banca_visible, "Banca")
        mostrar_mano(cartas_jugador_valores, cartas_jugador_palos, cantidad_cartas_jugador, puntaje_jugador, nombre_jugador)

        jugador_se_paso = False
        es_turno_jugador = True
        while es_turno_jugador:
            if puntaje_jugador == 21:
                print("¡21! Pasa el turno a la banca automáticamente.")
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
            registrar_resultado(ALJ, pos_jugador, 2, False, 0)
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
                registrar_resultado(ALJ, pos_jugador, 2, True, 0)
            elif puntaje_banca > puntaje_jugador:
                print("La banca gana la partida.")
                registrar_resultado(ALJ, pos_jugador, 2, False, 0)
            elif puntaje_banca < puntaje_jugador:
                print(nombre_jugador, "¡gana la partida!")
                registrar_resultado(ALJ, pos_jugador, 2, True, 0)
            else:
                print("¡Empate!")

        respuesta_usuario = input("¿Quiere jugar otra partida? (si/no): ").lower()
        while respuesta_usuario != "si" and respuesta_usuario != "no":
            respuesta_usuario = input("Entrada no válida. ¿Quiere jugar otra partida? (si/no): ").lower()
        quiere_jugar_de_nuevo = (respuesta_usuario == "si")

#-------------------------------------------------------------
# Juego 4: Dados - Par e Impar
#-------------------------------------------------------------
def leer_ganadas(ALJ, pos, juego):
    ALJ.seek(pos)
    RJ = pickle.load(ALJ)
    return RJ.juegos[0][juego]


def leer_creditos(ALJ, pos):
    ALJ.seek(pos)
    RJ = pickle.load(ALJ)
    return RJ.creditos


def dados_par_impar(ALJ):
    """ declarative de Variables utilizadas
    nombre_jugador, apuesta_texto, respuesta_par_impar, respuesta_usuario: string
    pos_jugador, monto_apuesta, dado1, dado2, suma_dados: int
    creditos_actuales: float
    juego_activo, resultado_es_par, jugador_acerto: bool
    """

    print("¡Bienvenido al juego de Par o Impar!")
    nombre_jugador = input("Ingrese su nombre: ")
    while nombre_jugador.strip() == "":
        nombre_jugador = input("El nombre no puede estar vacío. Ingrese su nombre: ")
    nombre_jugador = nombre_jugador.strip()

    pos_jugador = buscar_jugador(ALJ, nombre_jugador)
    if pos_jugador == -1:
        pos_jugador = alta_jugador(ALJ, nombre_jugador)
        print("Jugador nuevo registrado con 10000 créditos.")
    else:
        print("¡Bienvenido de nuevo,", nombre_jugador, "!")

    creditos_actuales = leer_creditos(ALJ, pos_jugador)

    if creditos_actuales <= 0:
        print(nombre_jugador, ", no te queda crédito disponible para jugar.")
    else:
        juego_activo = True
        while juego_activo and creditos_actuales > 0:
            print("Crédito actual de", nombre_jugador, ":", creditos_actuales)
            apuesta_texto = input("Ingrese cuanto quiere apostar: ")
            while (not apuesta_texto.isdigit()) or int(apuesta_texto) <= 0 or int(apuesta_texto) > creditos_actuales:
                apuesta_texto = input("Apuesta inválida. Ingrese un monto entre 1 y " + str(int(creditos_actuales)) + ": ")
            monto_apuesta = int(apuesta_texto)

            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
            suma_dados = dado1 + dado2

            respuesta_par_impar = input(nombre_jugador + ", ingrese si el resultado de la suma de los dados es par o impar: ").lower()
            while respuesta_par_impar != "par" and respuesta_par_impar != "impar":
                respuesta_par_impar = input("Entrada no válida. Ingrese 'par' o 'impar': ").lower()

            resultado_es_par = (suma_dados % 2 == 0)
            jugador_acerto = (respuesta_par_impar == "par" and resultado_es_par) or (respuesta_par_impar == "impar" and not resultado_es_par)

            if jugador_acerto:
                print(nombre_jugador, "¡Correcto! El resultado fue:", suma_dados)
                registrar_resultado(ALJ, pos_jugador, 3, True, monto_apuesta)
            else:
                print(nombre_jugador, "¡Incorrecto! El resultado fue:", suma_dados)
                registrar_resultado(ALJ, pos_jugador, 3, False, -monto_apuesta)

            creditos_actuales = leer_creditos(ALJ, pos_jugador)

            if creditos_actuales <= 0:
                print(nombre_jugador, "se quedó sin crédito. ¡Juego terminado!")
                juego_activo = False
            else:
                respuesta_usuario = input("¿Quiere seguir jugando? (si/no): ").lower()
                while respuesta_usuario != "si" and respuesta_usuario != "no":
                    respuesta_usuario = input("Entrada no válida. ¿Quiere seguir jugando? (si/no): ").lower()
                juego_activo = (respuesta_usuario == "si")

        print(nombre_jugador, "finalizó el juego con un crédito de", creditos_actuales, "y", leer_ganadas(ALJ, pos_jugador, 3), "aciertos totales.")

#-------------------------------------------------------------
# Juego 5: Reporte
#-------------------------------------------------------------
def contar_jugadores(ALJ):
    t = tamanio_archivo(ALJ)
    cantidad = 0
    ALJ.seek(0)
    while ALJ.tell() < t:
        pickle.load(ALJ)
        cantidad += 1
    return cantidad

def reporte_creditos(ALJ):
    """ declarative de Variables utilizadas
    nombres_ordenados: arr[string]
    creditos_ordenados: arr[float]
    cantidad, i, j: int
    RJ: Jugadores
    """

    cantidad = contar_jugadores(ALJ)

    if cantidad == 0:
        print("No hay jugadores registrados.")
    else:
        nombres_ordenados = [""] * cantidad
        creditos_ordenados = [0.0] * cantidad

        ALJ.seek(0)
        for i in range(cantidad):
            RJ = pickle.load(ALJ)
            nombres_ordenados[i] = RJ.nombre.strip()
            creditos_ordenados[i] = RJ.creditos

        # Burbujeo: de mayor a menor
        for i in range(cantidad - 1):
            for j in range(cantidad - 1 - i):
                if creditos_ordenados[j] < creditos_ordenados[j + 1]:
                    creditos_ordenados[j], creditos_ordenados[j + 1] = creditos_ordenados[j + 1], creditos_ordenados[j]
                    nombres_ordenados[j], nombres_ordenados[j + 1] = nombres_ordenados[j + 1], nombres_ordenados[j]

        print("\n--- Jugadores ordenados por créditos (de mayor a menor) ---")
        for i in range(cantidad):
            print(nombres_ordenados[i], "- Créditos:", creditos_ordenados[i])

def reporte_juegos_jugador(ALJ):
    """ declarative de Variables utilizadas
    nombre_jugador: string
    nombres_juegos: arr[string]
    pos_jugador, juego, ganadas, perdidas: int
    jugo_alguno: bool
    RJ: Jugadores
    """

    nombres_juegos = [""] * 4
    nombres_juegos[0] = "Mayor o Menor"
    nombres_juegos[1] = "Número Secreto"
    nombres_juegos[2] = "Blackjack"
    nombres_juegos[3] = "Par o Impar"

    nombre_jugador = input("Ingrese el nombre del jugador a consultar: ")
    while nombre_jugador.strip() == "":
        nombre_jugador = input("El nombre no puede estar vacío. Ingrese el nombre del jugador: ")
    nombre_jugador = nombre_jugador.strip()

    pos_jugador = buscar_jugador(ALJ, nombre_jugador)

    if pos_jugador == -1:
        print("El jugador", nombre_jugador, "no está registrado.")
    else:
        ALJ.seek(pos_jugador)
        RJ = pickle.load(ALJ)

        print("\n--- Juegos jugados por", RJ.nombre.strip(), "---")
        jugo_alguno = False
        for juego in range(4):
            ganadas = RJ.juegos[0][juego]
            perdidas = RJ.juegos[1][juego]
            if ganadas + perdidas > 0:
                print(nombres_juegos[juego], "- Ganó:", ganadas, "- Perdió:", perdidas)
                jugo_alguno = True

        if not jugo_alguno:
            print("Todavía no jugó ninguna partida.")
        print("Créditos que le quedan:", RJ.creditos)


def menu_reporte():
    print("\nREPORTE")
    print("A. Lista de jugadores ordenados de mayor a menor por créditos")
    print("B. Juegos jugados por un jugador")
    print("C. Volver al menú principal")

def reporte(ALJ):
    """ declarative de Variables utilizadas
    opc: string
    """

    opc = ""
    while opc != "C":
        menu_reporte()
        opc = input("Ingrese su opción: ").upper()
        while opc != "A" and opc != "B" and opc != "C":
            opc = input("Ingreso inválido - reintente: ").upper()

        limpiar_consola()

        if opc == "A":
            reporte_creditos(ALJ)
        elif opc == "B":
            reporte_juegos_jugador(ALJ)
#-------------------------------------------------------------
# F. Administración de Juegos
#-------------------------------------------------------------

def rellenar(texto, largo):
    """ Completa con espacios hasta que el texto ocupe 'largo' BYTES.
    Importante: ljust cuenta caracteres, pero las tildes ocupan 2 bytes al guardarse.
    Si el registro cambia de tamaño, al modificarlo en el archivo se pisa el siguiente.
    """
    return texto + " " * (largo - len(texto.encode("utf-8")))

def entra_en(texto, largo):
    return len(texto.encode("utf-8")) <= largo

def pedir_texto(mensaje, largo):
    """ declarative de Variables utilizadas
    texto: string
    """
    texto = input(mensaje).strip()
    while texto == "" or not entra_en(texto, largo):
        if texto == "":
            print("El dato no puede estar vacío.")
        else:
            print("El dato supera el máximo de", largo, "caracteres.")
        texto = input(mensaje).strip()
    return texto

def pedir_opcion(maxima):
    """ declarative de Variables utilizadas
    opc: string
    """
    opc = input("Ingrese su opción: ")
    while (not opc.isdigit()) or int(opc) < 1 or int(opc) > maxima:
        opc = input("Ingreso inválido - reintente: ")
    return int(opc)

#-------------------------------------------------------------
# Contraseña de administrador (oculta, 3 intentos)
#-------------------------------------------------------------
def validar_clave():
    """ declarative de Variables utilizadas
    clave: string
    intentos: int
    acceso: bool
    """
    intentos = 0
    acceso = False
    while intentos < 3 and not acceso:
        clave = getpass.getpass("Ingrese la contraseña de administrador: ")
        if clave == CLAVE_ADMIN:
            acceso = True
        else:
            intentos += 1
            if intentos < 3:
                print("Contraseña incorrecta. Intentos restantes:", 3 - intentos)
    if not acceso:
        print("Superó los 3 intentos de ingresar contraseña, salga e intente nuevamente")
    return acceso

#-------------------------------------------------------------
# Búsquedas y listados de categorías
#-------------------------------------------------------------
def listar_categorias(ALC, solo_activas):
    """ declarative de Variables utilizadas
    t, cantidad: int
    RC: Categorias
    """
    cantidad = 0
    t = tamanio_archivo(ALC)
    ALC.seek(0)
    while ALC.tell() < t:
        RC = pickle.load(ALC)
        if RC.estado == "A" or not solo_activas:
            print(RC.nrocategoria, "-", RC.nombrecategoria.strip(), "(" + RC.estado + ")")
            cantidad += 1
    return cantidad

def buscar_categoria_pos(ALC, nro, solo_activas):
    """ Devuelve la posición del registro de la categoría, o -1 si no existe
    (o si solo_activas y no está en estado "A") """
    pos_encontrada = -1
    t = tamanio_archivo(ALC)
    ALC.seek(0)
    while ALC.tell() < t and pos_encontrada == -1:
        pos_actual = ALC.tell()
        RC = pickle.load(ALC)
        if RC.nrocategoria == nro and (RC.estado == "A" or not solo_activas):
            pos_encontrada = pos_actual
    return pos_encontrada

def existe_nombre_categoria(ALC, nombre, nro_excluir):
    """ True si ya hay otra categoría con ese nombre (sin distinguir mayúsculas) """
    existe = False
    t = tamanio_archivo(ALC)
    ALC.seek(0)
    while ALC.tell() < t and not existe:
        RC = pickle.load(ALC)
        if RC.nrocategoria != nro_excluir and RC.nombrecategoria.strip().lower() == nombre.strip().lower():
            existe = True
    return existe

def proximo_nro_categoria(ALC):
    mayor = 0
    t = tamanio_archivo(ALC)
    ALC.seek(0)
    while ALC.tell() < t:
        RC = pickle.load(ALC)
        if RC.nrocategoria > mayor:
            mayor = RC.nrocategoria
    return mayor + 1

def elegir_categoria(ALC, solo_activas):
    """ Muestra el listado y pide un número. Devuelve la posición del registro,
    o -1 si no hay categorías o el usuario cancela con 0.
    declarative de Variables utilizadas
    texto: string
    cantidad, pos: int
    cancelado: bool
    """
    pos = -1
    cantidad = listar_categorias(ALC, solo_activas)
    if cantidad == 0:
        print("No hay categorías para mostrar. Antes de registrar opciones se deben dar de alta categorías.")
    else:
        cancelado = False
        texto = input("Ingrese el número de categoría (0 para volver): ")
        while pos == -1 and not cancelado:
            if not texto.isdigit():
                print("Entrada no válida.")
            elif int(texto) == 0:
                cancelado = True
            else:
                pos = buscar_categoria_pos(ALC, int(texto), solo_activas)
                if pos == -1:
                    if solo_activas:
                        print("La categoría no existe o no está activa.")
                    else:
                        print("La categoría no existe.")
            if pos == -1 and not cancelado:
                texto = input("Ingrese otro número (0 para volver): ")
    return pos

#-------------------------------------------------------------
# Categorías: Alta - Modificación - Baja
#-------------------------------------------------------------
def categoria_alta(ALC):
    """ declarative de Variables utilizadas
    nombre, pregunta: string
    pos: int
    RC: Categorias
    """
    nombre = pedir_texto("Nombre de la nueva categoría: ", 30)
    if existe_nombre_categoria(ALC, nombre, 0):
        print("Ya existe una categoría con ese nombre. No se registró.")
    else:
        pregunta = pedir_texto("Pregunta (ej: ¿Quién tiene más años?): ", 200)
        RC = Categorias()
        RC.nrocategoria = proximo_nro_categoria(ALC)
        RC.nombrecategoria = rellenar(nombre, 30)
        RC.pregunta = rellenar(pregunta, 200)
        RC.estado = "A"
        pos = tamanio_archivo(ALC)
        ALC.seek(pos)
        pickle.dump(RC, ALC)
        ALC.flush()
        print("Categoría registrada con el número", RC.nrocategoria)

def categoria_modificacion(ALC):
    """ declarative de Variables utilizadas
    nombre: string
    pos: int
    RC: Categorias
    """
    print("\n--- Modificación de categoría ---")
    pos = elegir_categoria(ALC, True)
    if pos != -1:
        ALC.seek(pos)
        RC = pickle.load(ALC)
        print("Nombre actual:", RC.nombrecategoria.strip())
        nombre = pedir_texto("Nuevo nombre: ", 30)
        if existe_nombre_categoria(ALC, nombre, RC.nrocategoria):
            print("Ya existe otra categoría con ese nombre. No se modificó.")
        else:
            RC.nombrecategoria = rellenar(nombre, 30)
            ALC.seek(pos)
            pickle.dump(RC, ALC)
            ALC.flush()
            print("Categoría modificada.")

def categoria_baja(ALC):
    """ declarative de Variables utilizadas
    pos: int
    RC: Categorias
    """
    print("\n--- Baja de categoría ---")
    pos = elegir_categoria(ALC, True)
    if pos != -1:
        ALC.seek(pos)
        RC = pickle.load(ALC)
        RC.estado = "I"
        ALC.seek(pos)
        pickle.dump(RC, ALC)
        ALC.flush()
        print("La categoría", RC.nombrecategoria.strip(), "pasó a estado Inactiva.")

#-------------------------------------------------------------
# Opciones: Alta - Consulta
#-------------------------------------------------------------
def opciones_alta(ALC, ALO):
    """ declarative de Variables utilizadas
    objeto, valor_texto, respuesta: string
    pos_categoria, nro_categoria, pos: int
    otra: bool
    RC: Categorias
    RO: Opciones
    """
    print("\n--- Alta de opciones ---")
    pos_categoria = elegir_categoria(ALC, True)
    if pos_categoria != -1:
        ALC.seek(pos_categoria)
        RC = pickle.load(ALC)
        nro_categoria = RC.nrocategoria
        print("Categoría:", RC.nombrecategoria.strip())
        print("Pregunta:", RC.pregunta.strip())

        otra = True
        while otra:
            objeto = pedir_texto("Objeto (ej: Tom Cruise): ", 100)
            valor_texto = input("Valor numérico (ej: 61): ")
            while not valor_texto.isdigit():
                valor_texto = input("Valor inválido. Ingrese un número entero: ")

            RO = Opciones()
            RO.nrocategoria = nro_categoria
            RO.nroopcion = contar_opciones(ALO, nro_categoria) + 1
            RO.objeto = rellenar(objeto, 100)
            RO.valor = int(valor_texto)
            pos = tamanio_archivo(ALO)
            ALO.seek(pos)
            pickle.dump(RO, ALO)
            ALO.flush()
            print("Opción", RO.nroopcion, "registrada:", objeto, "-", RO.valor)

            respuesta = input("¿Cargar otra opción en esta categoría? (si/no): ").lower()
            while respuesta != "si" and respuesta != "no":
                respuesta = input("Entrada no válida. ¿Cargar otra opción? (si/no): ").lower()
            otra = (respuesta == "si")

def opciones_consulta(ALC, ALO):
    """ declarative de Variables utilizadas
    pos, t, contador: int
    RC: Categorias
    RO: Opciones
    """
    print("\n--- Consulta de opciones ---")
    pos = elegir_categoria(ALC, False)
    if pos != -1:
        ALC.seek(pos)
        RC = pickle.load(ALC)
        print("\nCategoría:", RC.nombrecategoria.strip())
        print("Pregunta:", RC.pregunta.strip())

        contador = 0
        t = tamanio_archivo(ALO)
        ALO.seek(0)
        while ALO.tell() < t:
            RO = pickle.load(ALO)
            if RO.nrocategoria == RC.nrocategoria:
                print(RO.nroopcion, "-", RO.objeto.strip(), ":", RO.valor)
                contador += 1

        if contador == 0:
            print("Esta categoría todavía no tiene opciones.")
        elif contador < 6:
            print("Atención: se necesitan al menos 6 opciones para poder jugar con esta categoría.")

#-------------------------------------------------------------
# Menús
#-------------------------------------------------------------
def menu_administracion():
    print("\nADMINISTRACIÓN DE JUEGOS")
    print("1. Administrar Categorías")
    print("2. Administrar Opciones")
    print("3. Volver")

def menu_categorias():
    print("\nADMINISTRAR CATEGORÍAS")
    print("1. Alta")
    print("2. Modificación")
    print("3. Baja")
    print("4. Volver")

def menu_opciones():
    print("\nADMINISTRAR OPCIONES")
    print("1. Alta")
    print("2. Consulta")
    print("3. Volver")

def administrar_categorias(ALC):
    opc = 0
    while opc != 4:
        menu_categorias()
        opc = pedir_opcion(4)
        if opc == 1:
            categoria_alta(ALC)
        elif opc == 2:
            categoria_modificacion(ALC)
        elif opc == 3:
            categoria_baja(ALC)

def administrar_opciones(ALC, ALO):
    opc = 0
    while opc != 3:
        menu_opciones()
        opc = pedir_opcion(3)
        if opc == 1:
            opciones_alta(ALC, ALO)
        elif opc == 2:
            opciones_consulta(ALC, ALO)

def administracion(ALC, ALO):
    """ declarative de Variables utilizadas
    opc: int
    """
    opc = 0
    if validar_clave():
        while opc != 3:
            menu_administracion()
            opc = pedir_opcion(3)
            if opc == 1:
                administrar_categorias(ALC)
            elif opc == 2:
                administrar_opciones(ALC, ALO)






#-------------------------------------------------------------
#Programa Principal
#-------------------------------------------------------------
""" declarative de Variables utilizadas
opc: string
"""

cartel()
cartel1()
input("Presione Enter para continuar...")

AFC = "C:\\tp3\\categorias.dat"
AFO = "C:\\tp3\\opciones.dat"
AFJ = "C:\\tp3\\jugadores.dat"
if not os.path.exists(AFC):
    ALC = open(AFC, "w+b")
else:
    ALC = open(AFC, "r+b")
if not os.path.exists(AFO):
    ALO = open(AFO, "w+b")
else:
    ALO = open(AFO, "r+b")
if not os.path.exists(AFJ):
    ALJ = open(AFJ, "w+b")
else:
    ALJ = open(AFJ, "r+b")

RC = Categorias()
RO = Opciones()
RJ = Jugadores()

opc = ""
while opc != "G":
    menu()
    opc = input("Ingrese su opcion: ").upper()
    while opc != "A" and opc != "B" and opc != "C" and opc != "D" and opc != "E" and opc != "F" and opc != "G":
        opc = input("Ingreso invalido - reintente: ").upper()

    limpiar_consola()

    match opc:
        case "A":
            mayor_menor(ALC, ALO, ALJ)
        case "B":
            numero_secreto(ALJ)
        case "C":
            blackjack(ALJ)
        case "D":
            dados_par_impar(ALJ)
        case "E":
            reporte(ALJ)
        case "F":
            administracion(ALC, ALO)
        case "G":
            print("Gracias por jugar, no apueste, juega por diversión")
            ALC.close()
            ALO.close()
            ALJ.close()
            input("Presione Enter para continuar...")
