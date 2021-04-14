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
from directKeys import  up, left, down, right
from directKeys import PressKey, ReleaseKey

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

# Se detiene la captura de video
vc.stop()
# Se cierran todas las ventanas
destroyAllWindows()