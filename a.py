#Integrantes:
    # - Agustin Franchini
    # - Nicolas Font
    # - Santino Manoni
    # - Ignacio Calcaterra Zagami

#Variables Utilizadas:
    # - 



#Importacion de librerias
import math
import random

#Carteles
def cartel():
    print("Bienvenidos a la casa de apuestas: 'El apostador feliz'")

def cartel1():
     print("¡Disclaimer!")
     print ("*Los juegos de apuestas estan prohibidos para los menores de edad!! y son perjudiciales para la salud*")

#Menu Principal
def menu():
    print("MENU PRINCIPAL")
    print("¿Qué juego quieres jugar?")
    print("1. Mayor o menor")
    print("2. Numero secreto")
    print("3. Blackjack")
    print("4. Dados - Par e Impar")
    print("5. Reporte")
    print("6. Salir")

#Juego 1: Mayor o Menor
def mayor_menor():
    print("¡Bienvenido al juego de Mayor o Menor!")
    nombre=input("Ingrese su nombre de usuario: ")
    numero_secreto = random.randint(1, 1000)
    cont_aciertos = 0
    bandera = True
    while bandera:
        intentos = str(input("Ingrese si el siguiente numero es mayor o menor: ").lower())
        if intentos == "mayor":
            if numero_secreto > numero_secreto:
                print("¡Correcto! El número secreto es mayor.")
                cont_aciertos += 1
            else:
                print("¡Incorrecto! El número secreto es menor.")
                bandera = False
        elif intentos == "menor":
            if numero_secreto < numero_secreto:
                print("¡Correcto! El número secreto es menor.")
                cont_aciertos += 1
            else:
                print("¡Incorrecto! El número secreto es mayor.")
                bandera = False
        else:
            print("Entrada no válida. Por favor, ingrese 'mayor' o 'menor'.")

#Programa Principal
