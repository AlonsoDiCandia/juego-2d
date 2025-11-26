import cv2

class Jugador:
    def __init__(self, personaje):
        self.x = personaje.x
        self.y = personaje.y
        self.ancho, self.largo = 50, 50
        self.W = 1000
        self.H = 500
        self.speed = 5
        self.image = None
        self.direccion = None
    
    def cambiar_imagen(self, personaje):
        logo = cv2.imread(personaje.imagen.path)
        if logo is None:
            raise FileNotFoundError("No se encontró imagen.")
        logo = cv2.resize(logo, (50, 50))
        self.image = logo
        self.lh, self.lw = logo.shape[:2]
        
    def actualizar_posicion(self, key, paredes):
        vx, vy = 0, 0
        if key == 'w':
            vy = -self.speed
        elif key == 's':
            vy = self.speed
        elif key == 'a':
            vx = -self.speed
        elif key == 'd':
            vx = self.speed

        direccion = ''
        if key in ['w', 's']:
            direccion = 'V'
        elif key in ['a', 'd']:
            direccion = 'H'
        
        if direccion == 'V':
            self.y += vy
        elif direccion == 'H':
            self.x += vx

        if self.colision(paredes):
            return self.x - vx, self.y - vy
        else:  
            self.x = max(0, min(self.W - self.lw, self.x))
            self.y = max(0, min(self.H - self.lh, self.y))

        return self.x, self.y

    ## Hacemos un barrido tanto por el eje x y por el eje y buscando paredes cercanas
    def paredes_cercanas(self, pared):
        if abs(self.x - pared.x + pared.ancho) < 20 or abs(self.x + 50 - pared.x) < 20 or abs(self.y - pared.y + pared.largo) < 20 or abs(self.y + 50 - pared.y) < 20:
            return True
        else:
            return False 
        
    def colision(self, paredes):
        ## Buscamos paredes cercanas para no iterar sobre el totoal de paredes todo el tiempo
        paredes = list(filter(self.paredes_cercanas, paredes))     
        print("Paredes encontradas:", len(paredes))

        if len(paredes) == 0:
            return False
        
        for p in paredes:
            if (self.x < p.x + p.ancho and self.x + self.ancho > p.x and self.y < p.y + p.largo and self.y + self.largo > p.y):
                return True
        return False
                
    
    