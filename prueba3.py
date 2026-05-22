#Juego Par o Impar

#Variables Utilizadas:
    # - nombre: string
    # - numero_secreto: int
    # - numero_secreto1: int
    # - bandera (jugando): bool
    # - lectura: string
    # - NRO: int (resultado de la suma de dos enteros)

import random

print("¡Bienvenido al juego de Par o Impar!")
nombre = input("Ingrese su nombre de usuario: ")
cont_aciertos = 0
jugando = True
while jugando:
    nro1 = random.randint(1, 6)
    nro2 = random.randint(1, 6)
    NRO = nro1 + nro2
    lectura = input("Ingrese si el resultado de la suma de los dados es par o impar: ").lower()

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
        