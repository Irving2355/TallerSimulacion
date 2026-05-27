import pygame
import sys

#comentario en linea
'''
comentario en bloque
'''
pygame.init()

#configuracion inicial
ANCHO = 800
ALTO = 600

NEGRO = (0,0,0)
BLANCO = (255,255,255)
ROJO = (255,0,0)
GRIS = (180,180,180)

FPS = 60

GRAVEDAD = 0.5
ITERACIONES = 5

PUNTO_LANZAMIENTO = pygame.Vector2(100, 450) 
RADIO_PROYECTIL = 10
FACTOR_DISPARO = 0.18
RADIO_IMPACTO = 18

pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

particulas = []

ligaduras = []

proyectiles = []

particula_seleccionada = None

simualacion_activa = False

arrastrando_disparo = False

pos_mouse_disparo = pygame.Vector2(PUNTO_LANZAMIENTO)

'''class Particula:
    def __init__(self,x,y):
        self.pos = pygame.Vector2(x,y)
        self.vel = pygame.Vector2(0,0)
    
    def actualizar(self):
        self.vel.y += 0.5
        self.pos += self.vel 

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, BLANCO, self.pos, 6)'''

class Particula:
    def __init__(self,x,y,fija=False):
        self.pos = pygame.Vector2(x,y)
        self.pos_anterior = pygame.Vector2(x,y)
        
        self.radio = 6
        
        self.fija = fija 
    
    def actualizar(self):
        if self.fija:
            return

        velocidad = self.pos - self.pos_anterior
        self.pos_anterior = self.pos.copy()
        
        self.pos = self.pos + velocidad + pygame.Vector2(0,GRAVEDAD)
    
    def dibujar(self, pantalla):
        if self.fija:
            color = ROJO
        else: 
            color = BLANCO
        
        pygame.draw.circle(pantalla, color, self.pos, self.radio) 

class Ligadura:
    def __init__(self, p1, p2):
        self.p1 = p1 
        self.p2 = p2 
        
        self.longitud = self.obtener_distancia()
    
    def obtener_distancia(self):
        return (self.p1.pos - self.p2.pos).length()
    
    def aplicar(self):
        delta = self.p2.pos - self.p1.pos 
        distancia = delta.length()
        
        if(distancia == 0):
            return

        diferencia = (self.longitud - distancia) / distancia
        correccion = delta * 0.5 * diferencia
        
        if not self.p1.fija:
            self.p1.pos -= correccion
        if not self.p2.fija:
            self.p2.pos += correccion 
    
    def dibujar(self, pantalla):
        pygame.draw.line(pantalla, GRIS, self.p1.pos, self.p2.pos, 2) 

class Proyectil:
    def __init__(self, pos, velocidad):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(velocidad)
        self.radio = RADIO_PROYECTIL
        self.activo = True
    
    def actualizar(self):
        if not self.activo:
            return
        #aplicamos euler
        self.vel.y += GRAVEDAD
        self.pos += self.vel
        
        if self.pos.x > ANCHO + 100 or self.pos.y > ALTO + 100:
            self.activo = False
        
        if self.pos.x < -100 or self.pos.y < -100:
            self.activo = False
        
    def dibujar(self, pantalla):
        if self.activo:
            pygame.draw.circle(pantalla, ROJO, self.pos, self.radio)


while True:
    reloj.tick(FPS)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            
            pos_mouse = pygame.Vector2(pygame.mouse.get_pos())
            
            if evento.button == 1:
                
                if (pos_mouse - PUNTO_LANZAMIENTO).length() < 30:
                    arrastrando_disparo = True
                    pos_mouse_disparo = pos_mouse
                else:
                    particula_seleccionada = None 
                    for p in particulas:
                        if(p.pos - pos_mouse).length() < 10:
                            particula_seleccionada = p
                            break
                
                    if particula_seleccionada is None:
                        particulas.append(Particula(pos_mouse.x, pos_mouse.y))
            
            if evento.button == 3:
                for p in particulas:
                    if(p.pos - pos_mouse).length() < 10:
                        p.fija = not p.fija
                        break 
            
            if evento.type == pygame.MOUSEMOTION:
                if arrastrando_disparo:
                    pos_mouse_disparo = pygame.Vector2(pygame.mouse.get_pos()) 
        #fin if de mousebuttondown
        
        if evento.type == pygame.MOUSEBUTTONUP:
            
            if evento.button == 1:
                if arrastrando_disparo:
                    pos_mouse = pygame.Vector2(pygame.mouse.get_pos())
                    
                    velocidad_inicial = (PUNTO_LANZAMIENTO - pos_mouse) * FACTOR_DISPARO
                    
                    proyectiles.append(Proyectil(PUNTO_LANZAMIENTO, velocidad_inicial))
                    
                    arrastrando_disparo = False
                    pos_mouse_disparo = pygame.Vector2(PUNTO_LANZAMIENTO) 
            
                elif particula_seleccionada is not None:
                    pos_mouse = pygame.Vector2(pygame.mouse.get_pos()) 
                    
                    for p in particulas:
                        if(p.pos - pos_mouse).length() < 10 and p != particula_seleccionada:
                            ligaduras.append(Ligadura(particula_seleccionada, p))
                            break
                    particula_seleccionada = None
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                simualacion_activa = not simualacion_activa
    #cilo de eventos cierre
    
    pantalla.fill(NEGRO)
    
    # for p in particulas:
    #     p.actualizar()
    #     p.dibujar(pantalla)
    
    if simualacion_activa:
        for p in particulas:
            p.actualizar()
        
        for i in range(ITERACIONES):
            for l in ligaduras:
                l.aplicar()
    
    for proyectil in proyectiles:
        proyectil.actualizar()
    
    #verificamos si choco con una particula
    for proyectil in proyectiles:
        if not proyectil.activo:
            continue
        
        for particula in particulas[:]:
            distancia = (proyectil.pos - particula.pos).length()
            if distancia < RADIO_IMPACTO:
                #if not particula.fija:
                    particulas.remove(particula)
                    ligaduras = [
                        l for l in ligaduras
                        if l.p1 != particula and l.p2 != particula
                    ]
                    proyectil.activo = False
                    break
    
    for l in ligaduras:
        l.dibujar(pantalla)
    
    for p in particulas:
        p.dibujar(pantalla)
    
    pygame.draw.circle(pantalla, ROJO, PUNTO_LANZAMIENTO, 8)
    
    if arrastrando_disparo:
        pygame.draw.line(pantalla, BLANCO, PUNTO_LANZAMIENTO,pos_mouse_disparo, 2)
        pygame.draw.circle(pantalla, BLANCO, pos_mouse_disparo,RADIO_PROYECTIL) 
    
    for proyectil in proyectiles:
        proyectil.dibujar(pantalla)
        
    proyectiles = [p for p in proyectiles if p.activo]
    
    pygame.display.flip()