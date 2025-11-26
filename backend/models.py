from django.db import models

# Create your models here.

class Personaje(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="statics")
    x = models.IntegerField()
    y = models.IntegerField()
    direccion = models.CharField(max_length=1)
    colision = models.BooleanField()
        
    def __str__(self):
        return self.nombre
    
class ImagenFondo(models.Model):
    nombre = models.CharField(max_length=50)
    # martriz = models.CharField(max_length=5000)
    paredes = models.ManyToManyField('Pared')
        
    def __str__(self):
        return self.nombre
    
class Pared(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    ancho = models.IntegerField()
    largo = models.IntegerField()
    direccion = models.CharField(max_length=1)  # 'H' o 'V'
    color = models.CharField(max_length=15, default='0,0,0')
        
    def __str__(self):
        return f"Pared en ({self.x}, {self.y})" 

class Bala(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    direccion = models.CharField(max_length=1)  # 'H' o 'V'
    vector = models.BooleanField()
    imagen_fondo = models.ForeignKey('ImagenFondo', on_delete=models.CASCADE)