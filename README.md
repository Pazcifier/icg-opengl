# ICG-paz-engine
## Introducción
El siguiente es un documento que describe el proyecto de curso de la materia Introducción a la Computación Gráfica (de ahora en adelante “engine”)

El siguiente presenta las herramientas utilizadas, estructura del proyecto, manual de uso y consideraciones para próximas versiones y refinamiento.

## Herramientas utilizadas
El engine se desarrolló en **Python 3.7.0 32-bit** utilizando el IDE **Visual Studio Code** en su versión **1.5.1**, el proyecto posee dos dependencias externas extra:
- **PyGame v. 1.9.6**, un framework para el desarrollo de videojuegos en el lenguaje Python, utilizando principalmente para campos de visión y lectura de teclas (o eventos)
- **PyOpenGL v. 3.1.5**, un framework que traduce las funcionalidades de OpenGL al lenguaje Python

Si se desea, el proyecto viene con un entorno virtual con la versión **Python 3.6.0**

## Estructura
### Del proyecto
El proyecto está conformado por un archivo principal **main.py** en donde se realiza la carga inicial de los modelos, sus texturas y animaciones, además de la lectura de eventos, configuraciones de luz, shading y dibujado.

Dentro del mismo proyecto, hay otras módulos internos que son utilizadas para hacer el funcionamiento del engine posible:
- Carpeta **assets**, que contiene todos los elementos que se van a cargar, dentro de ella se separan las carpetas de:
    - **models** para los archivos .obj
    - **textures** para las texturas de un objeto
    - **animations** para los frames de animación de un objeto 

Las dos últimas contienen módulos dependiendo del modelo que le pertenezcan.
- Carpeta **camera**, contiene dos implementaciones de cámaras que fueron las vistas en clases: 
    - **fps.py** que contiene la implementación de una cámara en primera persona
    - **trackBall.py** que contiene la implementación de una cámara en tercera persona
- Carpeta **controller**, contiene todos los controladores, se entiende controlador a un archivo principal donde se guardan todos los datos de un objeto para realizar una acción o referenciarlos de forma centralizada. Existen tres de ellos:
    - **objController.py**, encargado de controlar el objeto, guarda su modelo, animaciones, texturas, controles, cámara entre otros
    - **openglController.py** encargado de todas las operaciones del framework OpenGL, entre ellas la adición de luces, mapeo de texturas y operaciones de matrices
    - **animController.py** encargado de la reproducción de las animaciones a partir de la acción que se le provea
- Carpeta **handlers**, contiene los parsers y manejadores de los objetos, estos sirven más que nada para la carga inicial
    - **objHandler.py**, encargado de la carga del modelo principal del objeto, parsea el archivo .obj para obtener sus vértices, texturas y normales (la última versión es la **v4**)
    - **textureHandler.py**, encargado de la carga de texturas de un objeto, y añadir esos parámetros a la estructura principal del objeto (la última versión es la **v3**)
    - **animationHandler.py**, encargado de la carga de cada uno de los frames y el ordenamiento de ellos, además de la adición de estos parámetros en la estructura principal del objeto
- Carpeta **referencias**, contiene referencias vistas en clases y otros archivos que profundizan en aspectos del proyecto

### Del objeto
El objeto utiliza los **diccionarios** como estructura de datos, donde agregamos cada uno de los datos obtenidos del objeto. Un objeto tiene como mínimo un modelo y ciertos metadatos para poder ser renderizado, a medida que se agregan otros parámetros, como texturas o animaciones estos se van agregando a la estructura de datos. Se realiza de esta manera para que un objeto no necesite tener todas las piezas para poder ser renderizado.

Para tener una vista completa de la estructura del objeto, mirar el archivo **estructura de obj.txt** dentro de la carpeta **referencias**

## Manual de Uso
### Ejecución
Para ejecutar, escribir el comando `python main.py` en la carpeta principal del engine. Se abrirá una pantalla en blanco y en la consola se mostrarán logs sobre el proceso actual de carga.

Al finalizar la carga aparecerá una escena con cielo azul y un plano de césped, contiene luces blancas y rojas y tres modelos, dos **knight** cada uno con una textura distinta y un **hueteotl** que es el jugador principal.

### Controles
- Para mover al jugador hacia adelante o hacia atrás presionar **W** o **S** respectivamente
- Para rotar al jugador hacia la izquierda o hacia la derecha presionar **A** o **D** respectivamente
- Para rotar la cámara hacia la izquierda o hacia la derecha presionar la **flecha Izquierda** o la **flecha Derecha** respectivamente
- Para agacharse, presionar cualquiera de las teclas **Control**
- Para saltar, presionar la tecla **Space** o **Espacio**
- Para alabar, presionar la **flecha Arriba**
- Para provocar, presionar la **flecha Abajo**
- Para salir, presionar la tecla **Esc**

### Interno
- Todo empieza creando un **objController** para cada modelo, dentro de él existen funciones para **cargar** modelos, texturas y animaciones.
- Se realizan configuraciones de **OpenGL**, en específico de **luz**, **renderizado**, y **color de fondo**
- Se inicia el **ciclo principal** donde comenzamos leyendo las **entradas del usuario** y **preparación de la escena**
- Se preparan los modelos con la **animación** correspondiente
- Se **dibujan** los modelos

## Consideraciones
- Aunque la animación sea continua, el movimiento no, se puede mantener la tecla **W** o **S** para reproducir la animación pero no se moverá más de un espacio, lo mismo ocurre con las rotaciones
- La cámara en tercera persona del jugador no se mueve referente a la rotación del objeto, lo que puede causar resultados extraños a la hora de moverse en ángulos distintos a 0 y 180 grados
- Es difícil dibujar sobre la escena y tener en mente posiciones relativas, escalados, etc. Sería de gran ayuda poseer un manejador de escenas (archivo en la carpeta handlers pero solo contiene notas e ideas)
- Tarda mucho en realizar la carga inicial, sería de gran ayuda ver una manera de cargar de forma paralela
- Realizar optimizaciones debido a que mientras más objetos hay, más lento son las lecturas del usuario
