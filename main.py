import pygame
import sys
import random

# Inicializa Pygame
pygame.init()

# Establece la resolución de la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Establece el título de la ventana
pygame.display.set_caption("Ping Pong")

# Define algunos colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
MORADO = (128, 0, 128)

# Define la paleta
paleta = pygame.Rect(375, 550, 100, 20)

# Define la pelota
pelota = pygame.Rect(400, 300, 20, 20)
velocidad_pelota = [5, 5]

# Define los enemigos
enemigos = []
colores_enemigos = [ROJO, VERDE, AZUL, AMARILLO, MORADO]

# Define el marcador
puntos = 0
fuente = pygame.font.Font(None, 36)

def mostrar_menu():
    opciones = ["Comenzar Juego", "Salir"]
    seleccion = 0

    while True:
        pantalla.fill(NEGRO)
        fuente_menu = pygame.font.Font(None, 74)
        texto_titulo = fuente_menu.render("Ping Pong", True, BLANCO)
        pantalla.blit(texto_titulo, (250, 150))

        fuente_opciones = pygame.font.Font(None, 50)
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (100, 100, 100)
            texto_opcion = fuente_opciones.render(opcion, True, color)
            pantalla.blit(texto_opcion, (350, 300 + i * 50))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return  # Comienza el juego
                    elif seleccion == 1:
                        pygame.quit()
                        sys.exit()

def reiniciar_juego():
    global puntos, pelota, velocidad_pelota, enemigos
    puntos = 0
    pelota = pygame.Rect(400, 300, 20, 20)
    velocidad_pelota = [5, 5]
    enemigos.clear()
    for _ in range(5):
        enemigos.append(pygame.Rect(random.randint(0, 780), random.randint(0, 400), 20, 20))

def juego():
    global puntos, pelota, velocidad_pelota, enemigos

    reiniciar_juego()
    en_pausa = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_p]:
            en_pausa = not en_pausa
            pygame.time.wait(200)  # Espera para evitar múltiples activaciones

        if not en_pausa:
            if teclas[pygame.K_LEFT]:
                paleta.x -= 5
            if teclas[pygame.K_RIGHT]:
                paleta.x += 5

            pelota.x += velocidad_pelota[0]
            pelota.y += velocidad_pelota[1]

            if pelota.colliderect(paleta):
                velocidad_pelota[1] = -velocidad_pelota[1]

            for i, enemigo in enumerate(enemigos):
                if pelota.colliderect(enemigo):
                    enemigos[i] = pygame.Rect(random.randint(0, 780), random.randint(0, 400), 20, 20)
                    velocidad_pelota[1] = -velocidad_pelota[1]
                    puntos += 20

            if pelota.x < 0 or pelota.x > 780:
                velocidad_pelota[0] = -velocidad_pelota[0]
            if pelota.y < 0:
                velocidad_pelota[1] = -velocidad_pelota[1]
            if pelota.y > 580:
                pantalla.fill(NEGRO)
                fuente_perdida = pygame.font.Font(None, 74)
                texto_perdida = fuente_perdida.render("¡PERDISTE!", True, BLANCO)
                pantalla.blit(texto_perdida, (250, 250))
                fuente_reinicio = pygame.font.Font(None, 36)
                texto_reinicio = fuente_reinicio.render("Presiona Espacio para Reiniciar", True, BLANCO)
                pantalla.blit(texto_reinicio, (250, 350))
                pygame.display.flip()

                while True:
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_SPACE:
                                reiniciar_juego()
                                break
                    else:
                        continue
                    break

            pantalla.fill(NEGRO)
            pygame.draw.rect(pantalla, BLANCO, paleta)
            pygame.draw.ellipse(pantalla, BLANCO, pelota)
            for i, enemigo in enumerate(enemigos):
                pygame.draw.rect(pantalla, colores_enemigos[i % len(colores_enemigos)], enemigo)

            texto_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
            pantalla.blit(texto_puntos, (10, 10))

        else:
            fuente_pausa = pygame.font.Font(None, 74)
            texto_pausa = fuente_pausa.render("PAUSADO", True, BLANCO)
            pantalla.blit(texto_pausa, (300, 250))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_RETURN:
                    return  # Reinicia el juego

# Mostrar el menú inicial
mostrar_menu()

# Comienza el juego
juego()
