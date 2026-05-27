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

#para generar la estructura
FUENTE = pygame.font.SysFont(None, 24)

BOTON_T_INVERTIDA = pygame.Rect(20, 20, 230, 35)

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


#funcion generada con Copilot
def crear_estructura_t_invertida():
    # Limpiamos la escena actual
    particulas.clear()
    ligaduras.clear()
    proyectiles.clear()

    # Diccionario para no crear partículas repetidas
    puntos = {}
    # Un diccionario en Python (dict) es la implementación 
    # nativa del lenguaje de las tablas hash 
    
    # Conjunto para no repetir ligaduras
    ligaduras_creadas = set()

    def crear_punto(x, y, fija=False):
        x = int(round(x))
        y = int(round(y))

        clave = (x, y)

        if clave in puntos:
            if fija:
                puntos[clave].fija = True
            return puntos[clave]

        p = Particula(x, y, fija)
        particulas.append(p)
        puntos[clave] = p
        return p

    def unir(p1, p2):
        if p1 == p2:
            return

        clave = tuple(sorted((id(p1), id(p2))))

        if clave not in ligaduras_creadas:
            ligaduras.append(Ligadura(p1, p2))
            ligaduras_creadas.add(clave)

    def crear_bloque(x, y, ancho, alto):
        """
        Crea un bloque rectangular usando 4 partículas
        y varias ligaduras.

        x, y representan la esquina superior izquierda.
        """

        arriba_izq = crear_punto(x, y)
        arriba_der = crear_punto(x + ancho, y)
        abajo_izq = crear_punto(x, y + alto)
        abajo_der = crear_punto(x + ancho, y + alto)

        # Bordes del bloque
        unir(arriba_izq, arriba_der)
        unir(abajo_izq, abajo_der)
        unir(arriba_izq, abajo_izq)
        unir(arriba_der, abajo_der)

        # Diagonales internas para que el bloque tenga rigidez
        unir(arriba_izq, abajo_der)
        unir(arriba_der, abajo_izq)

        return {
            "arriba_izq": arriba_izq,
            "arriba_der": arriba_der,
            "abajo_izq": abajo_izq,
            "abajo_der": abajo_der
        }

    # ==============================
    # Medidas principales
    # ==============================
    x_centro = 520

    y_suelo = 540
    y_plataforma = 455

    ancho_bloque = 75
    alto_bloque = 65
    espacio = 8

    # ==============================
    # 1. Soportes inferiores
    # Solo las partículas de abajo son fijas
    # ==============================

    x_soportes = [
        x_centro - 170,
        x_centro - 65,
        x_centro + 65,
        x_centro + 170
    ]

    puntos_superiores_soportes = []

    for x in x_soportes:
        abajo = crear_punto(x, y_suelo, fija=True)
        arriba = crear_punto(x, y_plataforma, fija=False)

        unir(abajo, arriba)

        puntos_superiores_soportes.append(arriba)

    # ==============================
    # 2. Plataforma horizontal
    # Como la madera de abajo en Angry Birds
    # ==============================

    x_inicio_plataforma = x_centro - 220
    x_fin_plataforma = x_centro + 220

    plataforma_izq = crear_punto(x_inicio_plataforma, y_plataforma)
    plataforma_der = crear_punto(x_fin_plataforma, y_plataforma)

    unir(plataforma_izq, plataforma_der)

    # Unimos los soportes con la plataforma
    for p in puntos_superiores_soportes:
        unir(plataforma_izq, p)
        unir(p, plataforma_der)

    # ==============================
    # 3. Primera fila de bloques
    # Tres bloques abajo
    # ==============================

    y_fila1 = y_plataforma - alto_bloque

    ancho_total_fila1 = 3 * ancho_bloque + 2 * espacio
    x_fila1 = x_centro - ancho_total_fila1 / 2

    bloque1 = crear_bloque(
        x_fila1,
        y_fila1,
        ancho_bloque,
        alto_bloque
    )

    bloque2 = crear_bloque(
        x_fila1 + ancho_bloque + espacio,
        y_fila1,
        ancho_bloque,
        alto_bloque
    )

    bloque3 = crear_bloque(
        x_fila1 + 2 * (ancho_bloque + espacio),
        y_fila1,
        ancho_bloque,
        alto_bloque
    )

    fila1 = [bloque1, bloque2, bloque3]

    # Conectar la primera fila con la plataforma
    for bloque in fila1:
        unir(bloque["abajo_izq"], plataforma_izq)
        unir(bloque["abajo_der"], plataforma_der)

        # Apoyos más directos hacia abajo
        punto_apoyo_izq = crear_punto(bloque["abajo_izq"].pos.x, y_plataforma)
        punto_apoyo_der = crear_punto(bloque["abajo_der"].pos.x, y_plataforma)

        unir(bloque["abajo_izq"], punto_apoyo_izq)
        unir(bloque["abajo_der"], punto_apoyo_der)

    # ==============================
    # 4. Segunda fila de bloques
    # Dos bloques al centro
    # ==============================

    y_fila2 = y_fila1 - alto_bloque

    ancho_total_fila2 = 2 * ancho_bloque + espacio
    x_fila2 = x_centro - ancho_total_fila2 / 2

    bloque4 = crear_bloque(
        x_fila2,
        y_fila2,
        ancho_bloque,
        alto_bloque
    )

    bloque5 = crear_bloque(
        x_fila2 + ancho_bloque + espacio,
        y_fila2,
        ancho_bloque,
        alto_bloque
    )

    fila2 = [bloque4, bloque5]

    # Conectar segunda fila con primera fila
    unir(bloque4["abajo_izq"], bloque1["arriba_der"])
    unir(bloque4["abajo_der"], bloque2["arriba_der"])

    unir(bloque5["abajo_izq"], bloque2["arriba_izq"])
    unir(bloque5["abajo_der"], bloque3["arriba_izq"])

    # Refuerzos diagonales entre niveles
    unir(bloque4["abajo_izq"], bloque2["arriba_izq"])
    unir(bloque4["abajo_der"], bloque1["arriba_der"])

    unir(bloque5["abajo_izq"], bloque3["arriba_izq"])
    unir(bloque5["abajo_der"], bloque2["arriba_der"])

    # ==============================
    # 5. Bloque superior
    # Un bloque arriba al centro
    # ==============================

    y_fila3 = y_fila2 - alto_bloque
    x_fila3 = x_centro - ancho_bloque / 2

    bloque6 = crear_bloque(
        x_fila3,
        y_fila3,
        ancho_bloque,
        alto_bloque
    )

    # Conectar bloque superior con segunda fila
    unir(bloque6["abajo_izq"], bloque4["arriba_der"])
    unir(bloque6["abajo_der"], bloque5["arriba_izq"])

    # Refuerzos diagonales del bloque superior
    unir(bloque6["abajo_izq"], bloque5["arriba_izq"])
    unir(bloque6["abajo_der"], bloque4["arriba_der"])

    # ==============================
    # 6. Refuerzos generales entre bloques vecinos
    # Esto hace que la estructura se parezca más a la imagen
    # ==============================

    # Unión entre bloques de la primera fila
    unir(bloque1["arriba_der"], bloque2["arriba_izq"])
    unir(bloque1["abajo_der"], bloque2["abajo_izq"])

    unir(bloque2["arriba_der"], bloque3["arriba_izq"])
    unir(bloque2["abajo_der"], bloque3["abajo_izq"])

    # Unión entre bloques de la segunda fila
    unir(bloque4["arriba_der"], bloque5["arriba_izq"])
    unir(bloque4["abajo_der"], bloque5["abajo_izq"])

while True:
    reloj.tick(FPS)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            
            pos_mouse = pygame.Vector2(pygame.mouse.get_pos())
            
            if evento.button == 1:
                
                #Evento para click izq y poder llamar la funcion
                if BOTON_T_INVERTIDA.collidepoint(pos_mouse):
                    crear_estructura_t_invertida()
                    continue
                
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
            #fin evento button = 1
            
            
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
    
    #dibujar el boton
    pygame.draw.rect(pantalla, GRIS, BOTON_T_INVERTIDA)
    pygame.draw.rect(pantalla, BLANCO, BOTON_T_INVERTIDA, 2)
    texto_boton = FUENTE.render("Crear T invertida", True, NEGRO)
    pantalla.blit(texto_boton, (BOTON_T_INVERTIDA.x + 20, BOTON_T_INVERTIDA.y + 8))
    
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