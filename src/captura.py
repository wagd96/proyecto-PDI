import cv2
import numpy as np

# Variable declarada para capturar el video en tiempo real de la camara
# Parametro '0' indica la webcam incorporada
vc = cv2.VideoCapture(0)
kernel = np.ones((5, 5), np.uint8)

# Conexion de camara wifi, usando la del celular
#  Android app: IP Webcam
#  En la ip se debe configurar el tamaño a 360x240 y modo espejo
address = "https://192.168.1.4:8080/video"
vc.open(address)

# Intervalos de color para un objeto Amarillo, en formato HSV (Tono, saturación, valor)
colormax = np.array([30, 255, 255], np.uint8)
colormin = np.array([20, 100, 100], np.uint8)

# Verde
# colormax = np.array([50,255,50])
# colormin = np.array([0,51,0])

# Rojo
# colormax = np.array([50,255,50])
# colormin = np.array([0,0,100])

# Azul
# colormax = np.array([255,120,120])
# colormin = np.array([40,0,0])

# redBajo1 = np.array([0, 100, 20], np.uint8)
# redAlto1 = np.array([8, 255, 255], np.uint8)
# redBajo2=np.array([175, 100, 20], np.uint8)
# redAlto2=np.array([179, 255, 255], np.uint8)

# Para la lectura de imagenes
while True:
    # Leemos el objeto y se asigna a
    # ret: la usaremos para detectar si se estan recibiendo o no imagenes
    # frame: es la imagen leida en milisegundos
    ret, frame = vc.read()

    # Se transforma la imagen capturada al espacio de color de BGR a HSV
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Con esta mascara haremos que cuando un pixel se encuentre dentro de nuestro intervalo
    #  va hacer un punto blanco, de lo contrario será un punto negro. Así detectados los puntos    
    maskColor = cv2.inRange(frameHSV, colormin, colormax)
    # Mascara de color
    maskColorvis = cv2.bitwise_and(frame, frame, mask= maskColor)

    # Se erosiona la imagen para eliminar impuresas captadas por la mascara
    maskColor = cv2.erode(maskColor, None, iterations=6)
    # Se dilata la imagen para regresar al tamaño original
    maskColor = cv2.dilate(maskColor, None, iterations=6)

    # Con esta instruccion eliminamos el ruido
    opening = cv2.morphologyEx(maskColor, cv2.MORPH_OPEN, kernel)
    
    # se crea el rectangulo
    x,y,w,h = cv2.boundingRect(opening)

    # Se dibujo el rectangulo y se pinta de color verde, grosor 4
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),4)

    # Se dibuja el circulo del centro, con grosor 6 y color rojo. El -1 es para rellenar
    cv2.circle(frame,(int(x+w/2),int(y+h/2)),6,(0,0,100),-1)

    # Se muestra la imagen captada
    cv2.imshow("webcam", frame)
    # Se muestra la imagen captada aplicandole las mascara
    cv2.imshow('maskColor', maskColor)
    # Se muestra la imagen captada mostrando solo el objeto de interes
    cv2.imshow('maskColorvis', maskColorvis)

    if cv2.waitKey(10)==27:
        break
destroyAllWindows()