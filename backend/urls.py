from django.urls import path
from .views import ListarPersonajesParaSeleccion, PersonajeSeleccionado, movimiento_personaje

urlpatterns = [
    path('seleccion-personaje/', ListarPersonajesParaSeleccion),
    path('personaje-seleccionado/<str:nombre>/', PersonajeSeleccionado),
    path('generar—movimiento/', movimiento_personaje)
]
