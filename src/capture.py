# --------------------------------------------------------------------------
# ------- CÓDIGO RECONOCIMIENTO DE CÁMARA ----------------------------------
# ------- Como controlador del juego 'Culebrita' ---------------------------
# ------- Coceptos básicos de PDI-------------------------------------------
# ------- PROCESAMIENTO DIGITAL DE IMÁGENES --------------------------------
# ------- Por:  Lina María Uribe lina.uribem@udea.edu.co -------------------
# -------       Alejandro Gallego wildey.gallego@udea.edu.co ---------------
# ------- Curso Básico de Procesamiento de Imágenes y Visión Artificial-----
# ------- Docente: David Fernández    david.fernandez@udea.edu.co ----------
# -------      Profesor Facultad de Ingenieria BLQ 21-409  -----------------
# -------      CC 71629489, Tel 2198528,  Wpp 3007106588 -------------------
# ------- Abril de 2021 ----------------------------------------------------
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# -- Se incluyen los paquetes necesarios para el programa ------------------
# --------------------------------------------------------------------------

import cv2
import numpy as np
import pyautogui
import pygame
import sys
from directKeys import  up, left, down, right
from directKeys import PressKey, ReleaseKey
from snake import Snake
from fruit import Fruit
from pygame.math import Vector2

# --------------------------------------------------------------------------
# -- Inicio Codificación del juego--- --------------------------------------
# --------------------------------------------------------------------------

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 18
screen = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load(
    '../resources/graphics/apple.png').convert_alpha()
game_font = pygame.font.Font(
    '../resources/font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
snake_velocity = 180
pygame.time.set_timer(SCREEN_UPDATE, snake_velocity)
snake = Snake(cell_size, screen)
fruit = Fruit(cell_number, cell_size, screen, apple)

def update():
    snake.move_snake()
    check_collision()
    check_fail()


def draw_elements():
    draw_grass()
    fruit.draw_fruit()
    snake.draw_snake()
    draw_score()


def check_collision():
    if fruit.pos == snake.body[0]:
        global snake_velocity
        fruit.randomize()
        snake.add_block()
        snake.play_crunch_sound()
        snake_velocity = snake_velocity - 3
        pygame.time.set_timer(SCREEN_UPDATE, snake_velocity)

    for block in snake.body[1:]:
        if block == fruit.pos:
            fruit.randomize()


def check_fail():
    if not -1 < snake.body[0].x < cell_number or not -1 < snake.body[0].y < cell_number:
        game_over()

    for block in snake.body[1:]:
        if block == snake.body[0]:
            game_over()


def game_over():
	global snake_velocity
	snake.reset()
	snake_velocity = 180
	pygame.time.set_timer(SCREEN_UPDATE, snake_velocity)


def draw_grass():
    grass_color = (167, 209, 61)
    for row in range(cell_number):
        if row % 2 == 0:
            for col in range(cell_number):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(
                        col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
        else:
            for col in range(cell_number):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(
                        col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)


def draw_score():
    score_text = str(len(snake.body) - 3)
    score_surface = game_font.render(score_text, True, (56, 74, 12))
    score_x = int(cell_size * cell_number - 60)
    score_y = int(cell_size * cell_number - 40)
    score_rect = score_surface.get_rect(center=(score_x, score_y))
    apple_rect = apple.get_rect(
        midright=(score_rect.left, score_rect.centery))
    bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                          apple_rect.width + score_rect.width + 6, apple_rect.height)

    pygame.draw.rect(screen, (167, 209, 61), bg_rect)
    screen.blit(score_surface, score_rect)
    screen.blit(apple, apple_rect)
    pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

# --------------------------------------------------------------------------
# -- Fin Codificación del juego --------------------------------------------
# --------------------------------------------------------------------------



# --------------------------------------------------------------------------
# -- Se inicializan variables ----------------------------------------------
# --------------------------------------------------------------------------

# Variable declarada para capturar el video en tiempo real de la cámara
# Parametro '0' indica la webcam incorporada
vc = cv2.VideoCapture(0)
kernel = np.ones((5, 5), np.uint8)

# Conexion de camara wifi (usando la del celular, Android app: IP Webcam)  
#  Se recomienda configurar en la ip el tamaño a 640x360 y modo espejo
#address = "https://192.168.1.3:8080/video"
#vc.open(address)

# Se establecen intervalos de color para un objeto Amarillo
#  En formato HSV (Tono, saturación, valor)
colormax = np.array([30, 255, 255], np.uint8)
colormin = np.array([20, 100, 100], np.uint8)

#set the initial values for parameter to use them later in the code
current_key = set()
# Se establece el radio del círculo para cubrir el objeto
radius_of_circle = 1
# Se establece el tamaño de la ventana del marco 
window_size = 160
# Se define la fuente de la letra con la que se escribirá en pantalla
font = cv2.FONT_HERSHEY_SIMPLEX


# --------------------------------------------------------------------------
# -- Lectura constante de la imagenes --------------------------------------
# --------------------------------------------------------------------------

while True:
    # Leemos el objeto en camara y se asigna:
    # ret: la usaremos para detectar si se estan recibiendo o no imagenes
    # frame: es la imagen leida en milisegundos
    ret, frame = vc.read()
    frame = cv2.flip(frame,1)
    # Se declaran variables con las dimensiones de la pantalla    
    height,width = frame.shape[:2]
    frame = cv2.resize(frame, dsize=(width, height))

    # Limites de las areas de juego Arriba, abajo, derecha e izquierda
    up_limit = (height/2 - window_size //2)
    down_limit = (height/2 + window_size //2)
    left_limit = (width/2 - window_size //2)
    right_limit = (width/2 + window_size //2)

    # Se aplica la función GaussianBlur para reducir el detalle de la imagen
    bluryellow_frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Se transforma la imagen capturada al espacio de color de BGR a HSV
    frameHSV = cv2.cvtColor(bluryellow_frame, cv2.COLOR_BGR2HSV)

    # Se establece una máscara de entre los intervalos de color
    # Con esta mascara haremos que cuando un pixel se encuentre dentro del intervalo
    #  será un punto blanco, de lo contrario será un punto negro
    #   Así detectados el objeto para jugar, obtiene el contorno con base en la máscara    
    mask = cv2.inRange(frameHSV, colormin, colormax)
    # Mascara usando el color original para los puntos seleccionados
    maskColor = cv2.bitwise_and(frame, frame, mask= mask)

    # Se erosiona la imagen para eliminar impuresas captadas por la máscara
    mask = cv2.erode(mask, None, iterations=6)
    maskColor = cv2.erode(maskColor, None, iterations=6)
    # Se dilata la imagen para regresar al tamaño original
    mask = cv2.dilate(mask, None, iterations=6)
    maskColor = cv2.dilate(maskColor, None, iterations=6)

    # Con esta instruccion eliminamos el ruido, realizando la operacion de apertura
    #  Esta operacion es hacer erosión seguida de dilatación
    # opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Se crea un rectángulo para encerrar el objeto detectado
    a,b,c,d = cv2.boundingRect(mask)

    # Se dibuja el rectangulo y se pinta de color amarillo con un grosor de 4
    cv2.rectangle(frame,(a,b),(a+c,b+d),(30, 255, 255),4)
    # Coordenadas del centro del objeto
    centre = (int(a+c/2),int(b+d/2))
    # Se dibuja un circulo en el centro del objeto, con grosor 6 y color rojo. El -1 es para rellenar
    cv2.circle(frame,centre,6,(0, 255, 0),-1)

    # --------------------------------------------------------------------------
    # -- Se halla la ubicación del jugador --------------------------------------
    # --------------------------------------------------------------------------
   
    # Para asegurarnos que todas las teclas queden liberadas al inicio del juego
    keyPressed = False
    keyPressed_lr = False         
            
    # Se establecen posiciones donde se detectarán las teclas arriba y abajo
    if centre[1] < up_limit and centre[1] > 0 and centre[0] > left_limit and centre[0] < right_limit:
        cv2.putText(frame ,'ARRIBA',(20,50),font,1,(255,255,255),2)
        # Para hacer click en la tecla ARRIBA con pyautogui
        pyautogui.press('up')
        current_key.add(up)
        keyPressed = True
        keyPressed_lr=True
    elif centre[1] > down_limit and centre[0] > left_limit and centre[0] < right_limit:
        cv2.putText(frame,'ABAJO',(20,50),font,1,(255,255,255),2)
        # Para hacer click en la tecla ABAJO con pyautogui
        pyautogui.press('down')
        current_key.add(down)
        keyPressed = True
        keyPressed_lr=True    
    # Se establecen posiciones donde se detectarán las teclas derecha e izquierda
    elif centre[1] > up_limit and centre[1] < down_limit and centre[0] < left_limit:
        cv2.putText(frame,'IZQUIERDA',(20,50),font,1,(255,255,255),2)
        # Para hacer click en la tecla IZQUIERDA con pyautogui
        pyautogui.press('left')
        keyPressed = True
        current_key.add(left)
    elif centre[1] > up_limit and centre[1] < down_limit and centre[0] > right_limit:
        cv2.putText(frame,'DERECHA',(20,50),font,1,(255,255,255),2)
        # Para hacer click en la tecla DERECHA con pyautogui
        pyautogui.press('right')
        keyPressed = True
        current_key.add(right)

    # Se liberan las teclas que hayan sido presionadas, para seguir jugando
    if not keyPressed and current_key!= 0:
        for key in current_key:
            ReleaseKey(key)
            current_key=set()

    # --------------------------------------------------------------------------
    # -- Se dibujan las areas de juego en el frame -----------------------------
    # --------------------------------------------------------------------------
    
    # Se dibuja el area para las acciones izquierda y derecha
    frame = cv2.rectangle(frame,(width//2 - window_size //2,0),(width//2 + window_size //2,height),(0,255,0),2)    
    # Se dibuja el area para las acciones de arriba y abajo
    frame= cv2.rectangle(frame,(0,height//2 - window_size //2),(width,height//2 + window_size //2),(255,0,0),2)

    # --------------------------------------------------------------------------
    # -- Se abren las ventanas para mostrar ------------------------------------
    # --------------------------------------------------------------------------
        
    # Se muestra la imagen captada con las areas de juego
    cv2.imshow("webcam", frame)
    # Se muestra la imagen captada aplicandole la mascara
    #cv2.imshow('mascara', mask)
    # Se muestra la imagen captada mostrando solo el objeto de interes
    cv2.imshow('mascaraColor', maskColor)

    # --------------------------------------------------------------------------
    # -- Se detiene el juego cuando el jugador así lo decida -------------------
    # --------------------------------------------------------------------------

    # Se termina el ciclo al presionar la tecla 'q'
    if cv2.waitKey(10)==ord('q'):
        break

    # --------------------------------------------------------------------------
    # -- Inicio de renderización del juego -------------------------------------
    # --------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake.direction.y != 1:
                    snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if snake.direction.x != -1:
                    snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if snake.direction.y != -1:
                    snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if snake.direction.x != 1:
                    snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    draw_elements()
    clock.tick(200)
    pygame.display.update()
    # --------------------------------------------------------------------------
    # -- FInal de renderización del juego --------------------------------------
    # --------------------------------------------------------------------------

# Se detiene la captura de video
vc.stop()
# Se cierran todas las ventanas
destroyAllWindows()