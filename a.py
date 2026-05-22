#Integrantes:
    # - Agustin Franchini
    # - Nicolas Font
    # - Santino Manoni
    # - Ignacio Calcaterra Zagami

#Importacion de librerias
import math
import random

#Carteles
def cartel():
    print("Bienvenidos a la casa de apuestas: 'El apostador feliz'")

def cartel1():
     print("¡Disclaimer!")
     print ("*Los juegos de apuestas estan prohibidos para los menores de edad!! y son perjudiciales para la salud*")

def cartel_opc3():
    print("¡Juego en desarrollo! Por favor, elija otra opción.")

#Menu Principal
def menu():
    print("MENU PRINCIPAL")
    print("¿Qué juego quieres jugar?")
    print("A. Mayor o menor")
    print("B. Numero secreto")
    print("C. Blackjack")
    print("D. Dados - Par e Impar")
    print("E. Reporte")
    print("S. Salir")

def reporte():
    print("¡Reporte en desarrollo! Por favor, elija otra opción.")

#Juego 1: Mayor o Menor
def mayor_menor():

    #Declaración de variables
    #nombre: str
    #numero_secreto: int
    #numero_secreto1: int
    #bandera: bool

    print("¡Bienvenido al juego de Mayor o Menor!")
    nombre=input("Ingrese su nombre de usuario: ")
    numero_secreto = random.randint(1, 1000)
    numero_secreto1 = random.randint(1, 1000)
    cont_aciertos = 0
    bandera = True
    while bandera:
            print("El número es:", numero_secreto)
            intentos = str(input("Ingrese si el siguiente numero es mayor o menor: ").lower())
            if intentos == "mayor":
                if numero_secreto < numero_secreto1:
                    print(nombre, "¡Correcto! El número secreto es mayor.")
                    cont_aciertos += 1
                else:
                    print(nombre, "¡Incorrecto! El número secreto es menor. El numero era:", numero_secreto1)
                    bandera = False
            elif intentos == "menor":
                if numero_secreto > numero_secreto1:
                    print(nombre, "¡Correcto! El número secreto es menor.")
                    cont_aciertos += 1
                else:
                    print(nombre, "¡Incorrecto! El número secreto es mayor. El numero era:", numero_secreto1)
                    bandera = False
            else:
                print("Entrada no válida. Por favor, ingrese 'mayor' o 'menor'.")
            numero_secreto = numero_secreto1
            numero_secreto1 = random.randint(1, 1000)

    print("¡Juego terminado!", nombre, " Has tenido: ", cont_aciertos, "aciertos.")

def numero_secreto():
    
    #Variables Utilizadas:
    # - nombre: string
    # - numero_secreto: int
    # - bandera (acertado): bool

    print("¡Bienvenido al juego Numero Secreto!")

    nombre = input("Ingrese su nombre de usuario: ")
    numero_secreto = random.randint(1, 100)
    intentos = 0
    max_intentos = 6
    cont_aciertos = 0
    acertado = False

    while intentos < max_intentos and not acertado:
        nro = int(input("Ingrese un número entre 1 y 100: "))
        intentos += 1

        if nro < numero_secreto:
            print(nombre, "¡El número secreto es mayor!")
            print("Intentos: ", max_intentos - intentos)

        elif nro > numero_secreto:
            print(nombre, "¡El número secreto es menor!")
            print("Intentos: ", max_intentos - intentos)

        else:
            print(nombre, "¡Felicidades! has adivinado el número secreto:", numero_secreto, "en", intentos, "intentos!")
            acertado = True

    if not acertado:
        print(nombre, "¡Lo siento! has agotado tus intentos! El número secreto era:", numero_secreto)

#juego 3: Blackjack
def blackjack():
    cartel_opc3()

#juego 4: Dados - Par e Impar
def dados_par_impar():
    #Juego Par o Impar

    #Variables Utilizadas:
        # - nombre: string
        # - numero_secreto: int
        # - numero_secreto1: int
        # - bandera (jugando): bool
        # - lectura: string
        # - NRO: int (resultado de la suma de dos enteros)

    print("¡Bienvenido al juego de Par o Impar!")
    nombre = input("Ingrese su nombre de usuario: ")
    cont_aciertos = 0
    jugando = True
    while jugando:
        nro1 = random.randint(1, 6)
        nro2 = random.randint(1, 6)
        NRO = nro1 + nro2
        lectura = input(nombre + ",Ingrese si el resultado de la suma de los dados es par o impar: ").lower()

        if lectura == "par":
            if NRO % 2 == 0:
                print(nombre, "¡Correcto! El resultado de la suma de los dados es par:", NRO)
                cont_aciertos += 1
            else:
                print(nombre, "¡Incorrecto! El resultado de la suma de los dados es impar. El resultado era:", NRO)
                jugando = False
        elif lectura == "impar":
            if NRO % 2 != 0:
                print(nombre, "¡Correcto! El resultado de la suma de los dados es impar:", NRO)
                cont_aciertos += 1
            else:
                print(nombre, "¡Incorrecto! El resultado de la suma de los dados es par. El resultado era:", NRO)
                jugando = False
        else:
            print("Entrada no válida. Por favor, ingrese 'par' o 'impar'.")

    print(nombre, "Juego terminado." " Has acertado:", cont_aciertos)
#Programa Principal
opc = "" 
while opc != "S":
    menu()
    opc = input("Ingrese su opcion: ").upper()
    while opc not in ["A", "B", "C", "D", "E", "S"]:
        opc = input("Ingreso invalido - reintente: ").upper()

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
            print("Gracias por jugar. Hasta luego!")
