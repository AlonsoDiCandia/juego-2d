from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import json

from .models import Personaje

# Create your views here.
from .generar_imagen.jugando_arucos import generar_imagen, cargar_paredes

def ListarPersonajesParaSeleccion(request):
    personajes = Personaje.objects.all()

    return render(request, 
                'seleccion_personaje.html',
                context={ "personajes": personajes })
    
def PersonajeSeleccionado(request, nombre):
    personaje = Personaje.objects.filter(nombre=nombre).first()

    return render(request, 
                  'personaje_seleccionado.html',
                  context={ 'personaje': personaje})

@csrf_exempt 
def movimiento_personaje(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}

        personaje = data.get("personaje")
        movimiento = data.get("movimiento")
        bala = data.get("bala")
        
        reset = True if movimiento == 'start' else False

        img, paredes = cargar_paredes(8, reset)
        imagen = generar_imagen(personaje, movimiento, img, paredes, bala) 

        _, buffer = cv2.imencode('.png', imagen)
        return HttpResponse(buffer.tobytes(), content_type='image/png')