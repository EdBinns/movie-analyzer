Instituto Tecnológico de Costa Rica <br>
Campus Tecnológico Local San Carlos <br>
Principios de Sistemas Operativos - II Semestre 2021 <br>

Proyecto creado por:
- Eduardo Binns Sánchez  [![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://github.com/EdBinns)
- Anthony Gariffith González  [![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://github.com/AnthonyGriffith)
- Andres Mora Barrantes  [![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://github.com/amorabarrantes)




# Analizador de peliculas con YOLO V3  

Al realizar este proyecto, se esperaba crear alguna forma de analizar peliculas con el fin de obtener escenas que contengan cierto tipo de imagenes buscadas. En este repositorio en particular se buscan imagenes que puedan llegar a ser sensibles para una audiencia menor de edad. Siendo ejemplo de esta problematica las pistolas, el fuego y los rifles.  

Con esta idea en mente, se empezo a indagar en la herramienta yolo y en como mejorarla mediante la aplicacion de hilos, y fueron obtenidos dos metodos.

 Division del video en frames
-------------
La idea de este metodo es primeramente dividir el video en cuestion en frames que seran almacenados en una lista, para posteriormente hacer un recorrido concurrente de la lista. Por lo cual cada hilo se encargara de un porcentaje equitativo del total de frames obtenidos del video.  

Sin embargo, una vez implementada esta posible solución, nos percatamos que no importaba cuantos hilos se agregaran o que porcentaje de los frames se asignaran a cada hilo, no hubo mejora con respecto a la forma secuencial de analizar los videos.
  
Multiples videos de forma concurrente  
-------------
Con este metodo lo que se busca es ejecutar multiples videos con YOLOv3 para de esta forma obtener una reducción de tiempo con respecto a la forma secuencial. Por lo cual, el tiempo de cada video como tal no se ve reducido, sino que al estar ejecutándose de forma paralela, el resultado en tiempo total de ejecución es menor a que si sumasemos individualmente la duracion de analisis del primer video con el analisis del segundo. 

En esta estrategia, es importante mencionar que no se guarda una imagen cada vez que se detecta un arma, puesto que en una misma escena se guardaría una gran cantidad de imágenes que representarían lo mismo y por lo tanto no sería adecuado. Lo que se realizó fue una estrategia en la cual si se detecta una pistola/rifle/fuego, se guarda la imagen solamente si en los últimos 120 frames no se ha detectado nada, en caso contrario de que ya se haya detectado un arma en los 120 frames anteriores, se procede a reiniciar el contador de frames. De esta forma en una escena de mucha acción violenta, solamente se guardaría una imagen con el tiempo en segundos en el cual fue detectada.

Para nuestra sorpresa, con este metodo se obtuvo una mejora significativa en el tiempo de analisis. La cual queda documentada en la seccion de mejoras.


Comparativa entre análisis secuencial vs paralelo.
-------------
<p align="center">
<img align="center" width="600" height="600" src="https://github.com/EdBinns/movie-analyzer/blob/main/imagenesGeneradas/Tiempo%20de%20ejecucion.png?raw=tru">
</p>
Como se puede observar, el tiempo de ejecucion de manera secuencial en comparacion con la concurrente, tiene un porcentaje de mejora de ~26%, puesto que de forma secuencial la suma de los analisis de los videos es de 2:30, y de forma concurrente es de 1:52.

Resultados de Detección
-------------

Los resultados que genera el proyecto se estaran almacenando en la carpeta Results que se encuentra dentro del proyecto
<p align="center">
<img align="center" width="400" height="400" src="https://github.com/EdBinns/movie-analyzer/blob/main/imagenesGeneradas/0-00-00.jpg?raw=true">
</p>

<p align="center">
<img align="center" width="400" height="400" src="https://github.com/EdBinns/movie-analyzer/blob/main/imagenesGeneradas/0-00-01.jpg?raw=true">
</p>

<p align="center">
<img align="center" width="400" height="400" src="https://github.com/EdBinns/movie-analyzer/blob/main/imagenesGeneradas/0-00-34.jpg?raw=true">
</p>

Tutorial
-------------
1: Clonar este repositorio de forma local.  
Vía http
``` 
https://github.com/EdBinns/movie-analyzer.git
```
Vía SSH
```
git@github.com:EdBinns/movie-analyzer.git
```
2: Con este comando, se instala OpenCv en el proyecto, el cual es necesario para el analisis de imagenes.  
```python
pip install opencv-python
``` 
3: Ingresar los videos de interés en la carpeta "Videos" del proyecto.  
4: Con este comando, el programa buscara la carpeta videos dentro del proyecto y utlizara todos los videos que se encuentren en está.  
```  
 python main.py --play_video True
```
