# Analizador de peliculas con YOLO V3.  

Al realizar este proyecto, se esperaba crear alguna forma de analizar peliculas con el fin de obtener escenas que contengan cierto tipo de imagenes buscadas. En este repositorio en particular se buscan imagenes que puedan llegar a ser sensibles para una audiencia menor de edad. Siendo ejemplo de esta problematica las pistolas, el fuego y los rifles.  

Con esta idea en mente, se empezo a indagar en la herramienta yolo y en como mejorarla mediante la aplicacion de hilos, y fueron obtenidos dos metodos.

 Division del video en frames:
-------------
La idea de este metodo es primeramente dividir el video en cuestion en frames que seran almacenados en una lista, para posteriormente hacer un recorrido concurrente de la lista. Por lo cual cada hilo se encargara de un porcentaje equitativo del total de frames obtenidos del video.  

Sin embargo, una vez implementada esta posible solución, nos percatamos que no importaba cuantos hilos se agregaran o que porcentaje de los frames se asignaran a cada hilo, no hubo mejora con respecto a la forma secuencial de analizar los videos.
  
Multiples videos de forma concurrente:  
-------------
En este caso, con este metodo se buscaba ejecutar multiples videos con YOLOv3. De esta manera se busca obtener resultados de reduccion de tiempo al intentar analizar mas de un video. Por lo cual, el tiempo de cada video no se ve reducido, sino que al estar ejecutandose a la vez, sumado el resultado concluimos que es menor el tiempo de ejecucion que si sumasemos independientemente la duracion de analisis de un video1 con el analisis de un video2.  

Para nuestra sorpresa, con este metodo se obtuvo una mejora significativa en el tiempo de analisis. La cual queda documentada en la seccion de mejoras.


Mejoras
-------------





https://github.com/EdBinns/movie-analyzer/blob/main/imagenesGeneradas/0-00-00.jpg?raw=true
