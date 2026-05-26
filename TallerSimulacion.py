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

pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

particulas = []

ligaduras = []

particula_seleccionada = None

simualacion_activa = False

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



while True:
    reloj.tick(FPS)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            
            pos_mouse = pygame.Vector2(pygame.mouse.get_pos())
            
            if evento.button == 1:
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
        #fin if de mousebuttondown
        
        if evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1 and particula_seleccionada is not None:
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
    
    for l in ligaduras:
        l.dibujar(pantalla)
    
    for p in particulas:
        p.dibujar(pantalla)
    
    pygame.display.flip()