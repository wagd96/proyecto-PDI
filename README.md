# CULEBRITA - INTERACCIÓN CON LA CÁMARA
[![Developed by @wagd96](https://img.shields.io/badge/developed%20by-%40AlejandroGallego-blue.svg  "Alejandro Gallego")](https://github.com/wagd96)   [![Developed by @linamariaum](https://img.shields.io/badge/developed%20by-%40linamariaum-b373ea.svg  "Lina María Uribe")](https://github.com/linamariaum)

Este proyecto se realiza para el curso Procesamiento Digital de Imágenes, semestre 2021-1, dictado por David Fernández ([david.fernandez@udea.edu.co](mailto:david.fernandez@udea.edu.co)), docente de la Facultad de Ingeniería en la [Universidad de Antioquia](http://udea.edu.co/).

> **Objetivo**
> * Identificar movimientos de un objeto usando procesamiento digital de imágenes para controlar el juego *Culebrita*. 
> Detección y el seguimiento del objeto en tiempo real.

Para esto se usó el juego *Snake* encontrado en [pygame.org](https://www.pygame.org/project/5398/7821), cuyo repositorio se encuentra en este [enlace](https://github.com/clear-code-projects/Snake). Adaptándolo con **OpenCV** para poder interactuar con este usando la cámara.

## Herramientas tecnológicas

El desarrollo se realiza en Python utilizando las siguientes librerías:
> * pygame
> * pyautogui
>  * opencv-python
>  * numpy

Estas se encuentran en el archivo ```requirements.txt```


## Técnicas empleadas del procesamiento digital de imágenes

1. Desenfoque gaussiano.
2. Espacio de color HSV.
3. Umbralización.
4. Erosión binaria.
5. Dilatación binaria.

En este video de YouTube se encuentra una explicación del proyecto así como de las técnicas empleadas para detectar la posición del objeto en cámara.

## Pasos para ejecutar el proyecto

Para ejecutar y jugar *Culebrita* es necesario tener un computador con una cámara conectada y un objeto de color amarillo

1. Clonar el proyecto.
2. Dirijirse al directorio del proyecto recién clonado.
3. Ejecutar en consola: 
	1.  `pip install -r requirements.txt`
	2.  `python capture.py`

Listo! Ahora para jugar solo debe mover un objeto de color **amarillo** dentro de las regiones para así mover la *Culebrita* hacia arriba, abajo, derecha o izquierda.

**Nota**: Para salir del juego puede oprimir la letra *q*.  

## Autores de la adaptación


|Nombre                |GitHub                          |Correo Electrónico|
|----------------|-------------------------------|-----------------------------|
|Lina María Uribe|[@linamariaum](https://github.com/linamariaum)            |*[lina.uribem@udea.edu.co](mailto:lina.uribem@udea.edu.co)*            |
|Alejandro Gallego Durango          |[@wagd96](https://github.com/@wagd96)           |*[wildey.gallego@udea.edu.co](mailto:wildey.gallego@udea.edu.co)*            |
