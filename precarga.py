#-------------------------------------------------------------
# PRECARGA de categorias.dat y opciones.dat
# Ejecutar UNA SOLA VEZ antes de entregar. Crea 3 categorías con 10 opciones cada una.
# ATENCIÓN: si los archivos ya existen, los reemplaza (se pierde lo que tuvieran).
#-------------------------------------------------------------
import pickle
import os
import os.path

CARPETA = "C:\\tp3\\"
AFC = CARPETA + "categorias.dat"
AFO = CARPETA + "opciones.dat"

# Las clases tienen que ser IGUALES a las del programa principal
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

def rellenar(texto, largo):
    # completa con espacios hasta 'largo' BYTES (las tildes ocupan 2)
    return texto + " " * (largo - len(texto.encode("utf-8")))

def agregar_categoria(ALC, nro, nombre, pregunta):
    RC = Categorias()
    RC.nrocategoria = nro
    RC.nombrecategoria = rellenar(nombre, 30)
    RC.pregunta = rellenar(pregunta, 200)
    RC.estado = "A"
    pickle.dump(RC, ALC)

def agregar_opcion(ALO, nro_categoria, nro_opcion, objeto, valor):
    RO = Opciones()
    RO.nrocategoria = nro_categoria
    RO.nroopcion = nro_opcion
    RO.objeto = rellenar(objeto, 100)
    RO.valor = valor
    pickle.dump(RO, ALO)

#-------------------------------------------------------------
# Programa principal de la precarga
#-------------------------------------------------------------
confirmar = "si"
if os.path.exists(AFC) or os.path.exists(AFO):
    confirmar = input("Los archivos ya existen y se van a REEMPLAZAR. ¿Continuar? (si/no): ").lower()

if confirmar == "si":
    if not os.path.exists(CARPETA):
        os.mkdir(CARPETA)

    ALC = open(AFC, "wb")
    ALO = open(AFO, "wb")

    # --- Categoría 1: goles en Mundiales (jugadores retirados, valores históricos) ---
    agregar_categoria(ALC, 1, "Goles en Mundiales", "¿Quién marcó más goles en Copas del Mundo?")
    agregar_opcion(ALO, 1, 1, "Miroslav Klose", 16)
    agregar_opcion(ALO, 1, 2, "Ronaldo Nazário", 15)
    agregar_opcion(ALO, 1, 3, "Gerd Müller", 14)
    agregar_opcion(ALO, 1, 4, "Just Fontaine", 13)
    agregar_opcion(ALO, 1, 5, "Pelé", 12)
    agregar_opcion(ALO, 1, 6, "Jürgen Klinsmann", 11)
    agregar_opcion(ALO, 1, 7, "Gabriel Batistuta", 10)
    agregar_opcion(ALO, 1, 8, "Roberto Baggio", 9)
    agregar_opcion(ALO, 1, 9, "Diego Maradona", 8)
    agregar_opcion(ALO, 1, 10, "Zinedine Zidane", 5)

    # --- Categoría 2: población (en millones, valores aproximados) ---
    agregar_categoria(ALC, 2, "Población de países", "¿Qué país tiene más habitantes (en millones)?")
    agregar_opcion(ALO, 2, 1, "India", 1450)
    agregar_opcion(ALO, 2, 2, "China", 1410)
    agregar_opcion(ALO, 2, 3, "Estados Unidos", 340)
    agregar_opcion(ALO, 2, 4, "Indonesia", 280)
    agregar_opcion(ALO, 2, 5, "Brasil", 212)
    agregar_opcion(ALO, 2, 6, "México", 129)
    agregar_opcion(ALO, 2, 7, "Japón", 124)
    agregar_opcion(ALO, 2, 8, "Alemania", 84)
    agregar_opcion(ALO, 2, 9, "Argentina", 46)
    agregar_opcion(ALO, 2, 10, "Chile", 19)

    # --- Categoría 3: altura de montañas (metros) ---
    agregar_categoria(ALC, 3, "Altura de montañas", "¿Qué montaña es más alta (en metros)?")
    agregar_opcion(ALO, 3, 1, "Everest", 8849)
    agregar_opcion(ALO, 3, 2, "K2", 8611)
    agregar_opcion(ALO, 3, 3, "Kangchenjunga", 8586)
    agregar_opcion(ALO, 3, 4, "Aconcagua", 6961)
    agregar_opcion(ALO, 3, 5, "Denali", 6190)
    agregar_opcion(ALO, 3, 6, "Kilimanjaro", 5895)
    agregar_opcion(ALO, 3, 7, "Elbrus", 5642)
    agregar_opcion(ALO, 3, 8, "Mont Blanc", 4806)
    agregar_opcion(ALO, 3, 9, "Cervino", 4478)
    agregar_opcion(ALO, 3, 10, "Monte Fuji", 3776)

    ALC.close()
    ALO.close()
    print("Listo: se cargaron 3 categorías y 30 opciones en", CARPETA)
else:
    print("No se modificó ningún archivo.")
