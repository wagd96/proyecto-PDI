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
import pyautogui
import numpy as np

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

# --------------------------------------------------------------------------
# -- Lectura constante de la imagenes --------------------------------------
# --------------------------------------------------------------------------

while True:
    # Leemos el objeto en camara y se asigna:
    # ret: la usaremos para detectar si se estan recibiendo o no imagenes
    # frame: es la imagen leida en milisegundos
    ret, frame = vc.read()

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

    # Se dibuja un circulo en el centro del objeto, con grosor 6 y color rojo. El -1 es para rellenar
    cv2.circle(frame,(int(a+c/2),int(b+d/2)),6,(0,0,100),-1)


    # --------------------------------------------------------------------------
    # -- Se haya la ubicación del jugador --------------------------------------
    # --------------------------------------------------------------------------

# -------------------- <MONO --------------------------------- 

    # encuentra los contornos de la mano
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Se definen los valores iniciales del centroide y del area encerrada por el contorno
    x, y, area = 0, 0, 0

    if len(contours) != 0:
        # Encontrar el contorno de area maxima(mano)
        cnt = max(contours, key=lambda x: cv2.contourArea(x))
        area = cv2.contourArea(cnt)

        if area > 200:
            # Obtener los momentos 
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                M["m00"] = 1
            
            # Se calcula la posición del centroide a partir de los momentos obtenidos
            x = int(M["m10"] / M["m00"])
            y = int(M['m01'] / M['m00'])

            # Se dibuja un circulo en donde está ubicado el centroide
            cv2.circle(frame, (x, y), 7, (255, 0, 0), 1)

            # Se define la fuente de la letra con la que se escribirá en pantalla
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Se escribe en pantalla las coordenadas del centroide y el área encerrada por el contorno
            cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, '{}'.format(area), (x + 10, y + 20), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)

# -------------------- MONO/> ---------------------------------


    # --------------------------------------------------------------------------
    # -- Se abren las ventanas para mostrar ------------------------------------
    # --------------------------------------------------------------------------

    # Se muestra la imagen captada
    cv2.imshow("webcam", frame)
    # Se muestra la imagen captada aplicandole la mascara
    #cv2.imshow('mascara', mask)
    # Se muestra la imagen captada mostrando solo el objeto de interes
    cv2.imshow('mascaraColor', maskColor)

    # --------------------------------------------------------------------------
    # -- Se detiene el juego cuando el jugador así lo decida -------------------
    # --------------------------------------------------------------------------

    # Se ermina el ciclo al presionar la tecla 'q'
    if cv2.waitKey(10)==ord('q'):
        break

# Se detiene la captura de video
vc.stop()
# Se cierran todas las ventanas
destroyAllWindows()