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
from game import Game
from directKeys import up, left, down, right
from directKeys import PressKey, ReleaseKey
from pygame.math import Vector2

# --------------------------------------------------------------------------
# -- Se inicializan variables ----------------------------------------------
# --------------------------------------------------------------------------

# Se inicia el juego
game = Game()

# Variable declarada para capturar el video en tiempo real de la cámara
# Parametro '0' indica la webcam incorporada
vc = cv2.VideoCapture(0)

# Se establecen intervalos de color para un objeto Amarillo
#  En formato HSV (Tono, saturación, valor)
colormax = np.array([30, 255, 255], np.uint8)
colormin = np.array([20, 100, 100], np.uint8)

# set the initial values for parameter to use them later in the code
current_key = set()
key_pressed = False
# Se establece el radio del círculo para cubrir el objeto
radius_of_circle = 1
# Se establece el tamaño de la ventana del marco
window_size = 80
# Se define la fuente de la letra con la que se escribirá en pantalla
font = cv2.FONT_HERSHEY_SIMPLEX

# Funcion para emular la accion de oprimir una tecla
def press_key(key, key_text):
    global key_pressed, current_key
    # Se muestra en pantalla la tecla que se oprimirá
    cv2.putText(frame, '{}'.format(key_text),
                (20, 50), font, 0.5, (255, 255, 255), 2)
    # Para hacer click en la tecla con pyautogui
    if key == 37:
        pyautogui.press('left')
    elif key == 38:
        pyautogui.press('up')
    elif key == 39:
        pyautogui.press('right')
    elif key == 40:
        pyautogui.press('down')
    current_key.add(key)
    key_pressed = True

# Funcion para liberar teclas oprimidas
def realese_key():
    global key_pressed, current_key
    # Se liberan las teclas que hayan sido presionadas, para seguir jugando
    if not key_pressed and current_key != 0:
        for key in current_key:
            ReleaseKey(key)
            current_key = set()
    key_pressed = False

# --------------------------------------------------------------------------
# -- Lectura  de imágenes de controles de juego-----------------------------
# --------------------------------------------------------------------------
arrows_control = cv2.imread('../resources/graphics/Controls.png')
pressed_left = cv2.imread('../resources/graphics/pressed_left.png')
pressed_up = cv2.imread('../resources/graphics/pressed_up.png')
pressed_right = cv2.imread('../resources/graphics/pressed_right.png')
pressed_down = cv2.imread('../resources/graphics/pressed_down.png')

# Variable que controlará el peso de las imágenes al fundirlas
alpha = 0.4

# --------------------------------------------------------------------------
# -- Lectura constante de la imágenes --------------------------------------
# --------------------------------------------------------------------------
while True:
    # Leemos el objeto en camara y se asigna:
    # ret: la usaremos para detectar si se estan recibiendo o no imágenes
    # frame: es la imagen leida en milisegundos
    ret, frame = vc.read()
    frame = cv2.flip(frame, 1)
    # Se declaran variables con las dimensiones de la pantalla
    height, width = frame.shape[:2]
    height = height//2
    width = width//2
    frame = cv2.resize(frame, dsize=(width, height))

    # Limites de las areas de juego Arriba, abajo, derecha e izquierda
    up_limit = (height/2 - window_size // 2)
    down_limit = (height/2 + window_size // 2)
    left_limit = (width/2 - window_size // 2)
    right_limit = (width/2 + window_size // 2)

    # Se aplica la función GaussianBlur para reducir el detalle de la imagen, desenfocar
    bluryellow_frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Se transforma la imagen capturada al espacio de color de BGR a HSV
    frameHSV = cv2.cvtColor(bluryellow_frame, cv2.COLOR_BGR2HSV)

    # Se establece una máscara de entre los intervalos de color
    # Con esta mascara haremos que cuando un pixel se encuentre dentro del intervalo
    #  será un punto blanco, de lo contrario será un punto negro
    #   Así detectados el objeto para jugar, obtiene el contorno con base en la máscara
    mask = cv2.inRange(frameHSV, colormin, colormax)
    # Mascara usando el color original para los puntos seleccionados
    maskColor = cv2.bitwise_and(frame, frame, mask=mask)

    # Se erosiona la imagen para eliminar impuresas captadas por la máscara
    mask = cv2.erode(mask, None, iterations=6)
    maskColor = cv2.erode(maskColor, None, iterations=6)
    # Se dilata la imagen para regresar al tamaño original
    mask = cv2.dilate(mask, None, iterations=6)
    maskColor = cv2.dilate(maskColor, None, iterations=6)

    # Se crea un rectángulo para encerrar el objeto detectado
    a, b, c, d = cv2.boundingRect(mask)

    # Se dibuja el rectangulo y se pinta de color amarillo con un grosor de 4
    cv2.rectangle(frame, (a, b), (a+c, b+d), (30, 255, 255), 4)
    # Coordenadas del centro del objeto
    centre = (int(a+c/2), int(b+d/2))
    # Se dibuja un circulo en el centro del objeto, con grosor 6 y color verde. El -1 es para rellenar
    cv2.circle(frame, centre, 6, (0, 255, 0), -1)

    # Mensaje en pantalla de bienvenida. Se muestra solo si no hay un objeto amarillo en pantalla.
    if centre == (0, 0):
        cv2.putText(frame, 'Bienvenido!', (8, 70),
                    font, 1.5, (30, 255, 255), 4)
        cv2.putText(frame, 'Usa un objeto',
                    (8, 140), font, 1, (30, 255, 255), 4)
        cv2.putText(frame, 'amarillo para', (8, 180),
                    font, 1, (30, 255, 255), 4)
        cv2.putText(frame, 'iniciar el juego.', (8, 220),
                    font, 1, (30, 255, 255), 4)

    # Para asegurarnos que todas las teclas queden liberadas al inicio del juego
    realese_key()

    # --------------------------------------------------------------------------
    # -- Se halla la ubicación del jugador -------------------------------------
    # --------------------------------------------------------------------------

    # Se establecen posiciones donde se detectarán las teclas arriba y abajo. Y se muestran los controles de juego, estos serán visibles solo si hay un objeto amarillo en pantalla.
    if(centre > (0, 0)):
        if centre[1] < up_limit and centre[1] > 0 and centre[0] > left_limit and centre[0] < right_limit:
            # Se presiona la tecla específica
            press_key(up, 'ARRIBA')
            # Se funde la imagen de controlador de juego en el frame de captura vídeo
            frame = cv2.addWeighted(frame, alpha, pressed_up, 1-alpha, 0)
        elif centre[1] > down_limit and centre[0] > left_limit and centre[0] < right_limit:
            press_key(down, 'ABAJO')
            frame = cv2.addWeighted(frame, alpha, pressed_down, 1-alpha, 0)
        # Se establecen posiciones donde se detectarán las teclas derecha e izquierda
        elif centre[1] > up_limit and centre[1] < down_limit and centre[0] < left_limit:
            press_key(left, 'IZQUIERDA')
            frame = cv2.addWeighted(frame, alpha, pressed_left, 1-alpha, 0)
        elif centre[1] > up_limit and centre[1] < down_limit and centre[0] > right_limit:
            press_key(right, 'DERECHA')
            frame = cv2.addWeighted(frame, alpha, pressed_right, 1-alpha, 0)
        else:
            frame = cv2.addWeighted(frame, alpha, arrows_control, 1-alpha, 0)

    # --------------------------------------------------------------------------
    # -- Se abren las ventanas para mostrar ------------------------------------
    # --------------------------------------------------------------------------

    # Se muestra la imagen captada con las areas de juego
    cv2.imshow("webcam", frame)
    # Se muestra la imagen captada mostrando solo el objeto de interes
    cv2.imshow('mascaraColor', maskColor)

    # --------------------------------------------------------------------------
    # -- Se detiene el juego cuando el jugador así lo decida -------------------
    # --------------------------------------------------------------------------

    # Se termina el ciclo al presionar la tecla 'q'
    if cv2.waitKey(10) == ord('q'):
        break

    # --------------------------------------------------------------------------
    # -- Inicio de renderización del juego -------------------------------------
    # --------------------------------------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == game.SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction.y != 1:
                    game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if game.snake.direction.x != -1:
                    game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if game.snake.direction.y != -1:
                    game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if game.snake.direction.x != 1:
                    game.snake.direction = Vector2(-1, 0)

    # Se define el color del fondo de la pantalla del juego
    game.screen.fill((175, 215, 70))
    # Se dibujan y actualizan constantemente los elementos del juego en pantalla
    game.draw_elements()
    game.clock.tick(200)
    pygame.display.update()
    # --------------------------------------------------------------------------
    # -- Final de renderización del juego --------------------------------------
    # --------------------------------------------------------------------------

# Se detiene la captura de video
vc.stop()
# Se cierran todas las ventanas
destroyAllWindows()

# ------------------------------------------------------------
# -------------  FIN DEL PROGRAMA ----------------------------
# ------------------------------------------------------------