import random

print("¡Bienvenido al juego de Mayor o Menor!")
nombre=input("Ingrese su nombre de usuario: ")
numero_secreto = random.randint(1, 1000)
numero_secreto1 = random.randint(1, 1000)
cont_aciertos = 0
bandera = True
while bandera:
        print("El número secreto es:", numero_secreto)
        intentos = str(input("Ingrese si el siguiente numero es mayor o menor: ").lower())
        if intentos == "mayor":
            if numero_secreto < numero_secreto1:
                print("¡Correcto! El número secreto es mayor.")
                cont_aciertos += 1
            else:
                print("¡Incorrecto! El número secreto es menor. El numero era:", numero_secreto1)
                bandera = False
        elif intentos == "menor":
            if numero_secreto > numero_secreto1:
                print("¡Correcto! El número secreto es menor.")
                cont_aciertos += 1
            else:
                print("¡Incorrecto! El número secreto es mayor. El numero era:", numero_secreto1)
                bandera = False
        else:
            print("Entrada no válida. Por favor, ingrese 'mayor' o 'menor'.")
        numero_secreto = numero_secreto1
        numero_secreto1 = random.randint(1, 1000)

print("¡Juego terminado!", nombre, " Has tenido: ", cont_aciertos, "aciertos.")