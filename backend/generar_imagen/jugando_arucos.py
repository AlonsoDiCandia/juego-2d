import cv2
import numpy as np
import time
import json
from random import randint

from .Jugador import Jugador
from .Pared import Pared
from ..models import Personaje, ImagenFondo, Bala
from ..models import Pared as ParedModel

H = 500
W = 1000

def generar_imagen(personaje, movimiento, img, paredes, bala):
    personaje = Personaje.objects.filter(nombre=personaje).first()
    jugador = Jugador(personaje)

    jugador.cambiar_imagen(personaje)

    # Tamaño del lienzo
    lh, lw = jugador.image.shape[:2]

    x,y = jugador.actualizar_posicion(movimiento, paredes)

    if bala:
        generar_bala(jugador, personaje.direccion)

    cargar_balas(img)

    personaje.x = x
    personaje.y = y
    personaje.direccion = movimiento if movimiento not in ['space', 'start'] else personaje.direccion


    personaje.save()

    img[y:y+lh, x:x+lw] = jugador.image

    return img

def cargar_paredes(numero_paredes, reset):
    img = np.full((H, W, 3), 255, dtype=np.uint8)

    img_obj = ImagenFondo.objects.get(nombre='background')
    
    if reset:
        img_obj.paredes.clear()
        for _ in range(numero_paredes):
            direccion = 'H' if randint(1,100) > 50 else 'V'

            x = randint(100, 900)
            y = randint(50, 450)
            ancho = randint(300, 600) if direccion == 'H' else 5
            largo = 5 if direccion == 'H' else randint(100, 400)

            pared_obj = ParedModel.objects.create(
                x = x,
                y = y,
                ancho = ancho,
                largo = largo,
                direccion = direccion
            )
            
            pared_obj.save()
            img_obj.paredes.add(pared_obj)
    
    paredes = img_obj.paredes.all()
    
    for pared in paredes:
        color = obtener_color(pared.color)
        if pared.direccion == 'H':
            cv2.line(img, (pared.x, pared.y), (pared.x + pared.ancho, pared.y), color, thickness=pared.largo) ## Agregar alto y ancho al modelo de Django
                
        if pared.direccion == 'V':
            cv2.line(img, (pared.x, pared.y), (pared.x, pared.y + pared.largo), color, thickness=pared.ancho) ## Agregar alto y ancho al modelo de Django

    return img, paredes

def obtener_color(color):
    color = color.split(',')
    return (int(color[0]), int(color[1]), int(color[2]))

def generar_bala(jugador, direccion):
    x_bala = jugador.x + (jugador.ancho / 2)
    y_bala = jugador.y + (jugador.largo / 2)
    vector = True
    img_obj = ImagenFondo.objects.get(nombre='background')
    if direccion in ['a', 'd']:
        if direccion == 'a':
            vector = False
    else:
        if direccion == 'w':
            vector = False

    bala_db = Bala.objects.create(
        x = x_bala,
        y = y_bala,
        direccion = 'H' if direccion in ['a', 'd'] else 'V',
        vector = vector,
        imagen_fondo = img_obj
    )

    bala_db.save()

def cargar_balas(img):
    img_obj = ImagenFondo.objects.get(nombre='background')
    balas = Bala.objects.filter(imagen_fondo = img_obj)
    for b in balas:
        if b.x >= W or b.x <= 0 or b.y >= H or b.y <= 0:
            b.delete()
            continue

        # print(b.x, b.y, b.direccion)
        x = b.x + (10 if b.vector else -10) if b.direccion == 'H' else b.x
        y = b.y + (10 if b.vector else -10) if b.direccion == 'V' else b.y

        b.x = x
        b.y = y

        b.save()
        
        cv2.circle(img, (x, y), 3, (0,0,0), -1)
    return img