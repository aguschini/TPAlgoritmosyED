import random
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
        print("¡El número secreto es mayor!")
        print("Intentos: ", max_intentos - intentos)

    elif nro > numero_secreto:
        print("¡El número secreto es menor!")
        print("Intentos: ", max_intentos - intentos)

    else:
        print("¡Felicidades:", nombre, "has adivinado el número secreto:", numero_secreto, "en", intentos, "intentos!")
        acertado = True

if not acertado:
    print("¡Lo siento:", nombre, "has agotado tus intentos! El número secreto era:", numero_secreto)
               