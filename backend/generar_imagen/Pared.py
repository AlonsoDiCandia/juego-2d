
class Pared:
    def __init__(self, x, y, direccion, largo):
        self.x = x
        self.y = y
        self.direccion = direccion
        self.color = (0, 0, 0)
        self.ancho = 0
        self.largo = 0
        
        if self.direccion == 'H':
            self.ancho = largo
            self.alto = 5
        elif self.direccion == 'V':
            self.ancho = 5
            self.alto = largo
