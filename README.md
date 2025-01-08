PAV - P4: reconocimiento y verificación del locutor
===================================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 4](https://github.com/albino-pav/P4)
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

También debe descomprimir, en el directorio `PAV/P4`, el fichero [db_8mu.tgz](https://atenea.upc.edu/mod/resource/view.php?id=3654387?forcedownload=1)
con la base de datos oral que se utilizará en la parte experimental de la práctica.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde
que los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
  run_spkid mfcc train test classerr verify verifyerr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recuerde que, además de los trabajos indicados en esta parte básica, también deberá realizar un proyecto
de ampliación, del cual deberá subir una memoria explicativa a Atenea y los ficheros correspondientes al
repositorio de la práctica.

A modo de memoria de la parte básica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.

### SPTK, Sox y los scripts de extracción de características.

- Analice el script `wav2lp.sh` y explique la misión de los distintos comandos involucrados en el *pipeline*
  principal (`sox`, `$X2X`, `$FRAME`, `$WINDOW` y `$LPC`). Explique el significado de cada una de las 
  opciones empleadas y de sus valores.

Este script genera los coeficientes LPC (extracción de características LPC) a partir de un archivo de audio en formato WAV. Utiliza herramientas de la biblioteca SPTK (Speech Signal Processing Toolkit) y se realiza mediante una canalización (pipeline) de comandos.
El archivo LPC comprimido, contiene los coeficientes lineales predictivos organizados en una matriz con encabezado.

→ **Comando SOX**: Convierte el archivo de entrada en formato WAV ($inputfile) a un flujo de datos de audio sin procesar en formato RAW.

-t raw:  formato de salida RAW (datos binarios sin encabezado).<br>
-e signed: datos de audio enteros con signo.<br>
-b 16: cada muestra de audio tiene un tamaño de 16 bits (profundidad).<br>
-: la salida será enviada al flujo estándar (stdout), para que pueda ser utilizada en la pipeline.

→ **Comando $X2X**: Convierte los datos binarios RAW generados por sox en números de coma flotante.  (+sf -> single-precision floating-point)

→ **Comando $FRAME**: Divide los datos de audio en _frames_ de longitud constante, permitiendo que cada uno sea procesado independientemente.

-l 240: longitud de cada frame -> 240 muestras (30 ms con una frecuencia de muestreo de 8 kHz).<br>
-p 80: desplazamiento (overlap) entre frames de 80 muestras (10 ms).<br>

→ **Comando $WINDOW**: Se enventana la señal con los siguientes parámetros.

-l 240: longitud de la señal de entrada (240 muestras).<br>
-L 240: longitud de la ventana (también 240 muestras).<br>

→ **Comando $LPC**: Realiza el análisis LPC sobre cada frame para obtener los coeficientes lineales predictivos. Estos coeficientes representan de forma compacta el espectro del audio.

-l 240: Longitud de la señal de entrada (240 muestras por frame).<br>
-m $lpc_order: Orden del análisis LPC (número de coeficientes).<br>


- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 49 a 55 del script `wav2lp.sh`).
  
Primero se determina el número de columnas del fichero de salida y el valor _lpc_order_ que representa el orden del análisis LPC. Luego, se suma 1 para incluir el coeficiente de ganancia (gain) en la primera columna.

En la siguiente linea se utiliza el comando _$X2X +fa_ para convertir los datos LPC almacenados en formato binario a texto flotante (ASCII). Además, los datos se leen desde el archivo _$base.lp_, que contiene los coeficientes LPC generados por SPTK.<br>
wc -l cuenta el número de líneas (valores) en el archivo convertido.
Posteriormente, se divide el número total de valores entre _ncol_ (número de columnas) para calcular el número de filas. Esta división garantiza que cada fila tenga exactamente _ncol_ valores.

El formato fmatrix requiere un encabezado con el número de filas y columnas, por eso el script añade esta información en el fichero.

  * ¿Por qué es más conveniente el formato *fmatrix* que el SPTK?

El formato fmatrix es más conveniente que el formato SPTK por varias razones: <br>
→ 1a: es autodescriptivo ya que incluye un encabezado que especifica el número de filas y columnas de la matriz. <br>
→ 2a: es portable, ya que sigue un esquema binario simple y bien definido (encabezado + datos). <br>
→ 3a: es fácil de usar con herramientas externas. <br>
→ 4a: organiza los datos en un formato matricial bien definido, lo que facilita su uso en algoritmos de machine learning, análisis estadístico o visualización. <br>
→ 5a: reduce errores al incluir información estructural explícita. <br>
    
- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:

  ![image](https://github.com/user-attachments/assets/b5ac1e0c-6a1e-4622-8501-629d3cbf2484)



- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:

  ![image](https://github.com/user-attachments/assets/1ff77b74-abaf-4fdc-bf2c-19af4e9c9483)


### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.

- PASO 1: Parametrización usando el script <code>run_spkid</code>:

![image](https://github.com/user-attachments/assets/6d6ffb62-745b-4e43-83e2-91354942054c)

![image](https://github.com/user-attachments/assets/e4f0638f-b330-4c96-8b4a-8d0f5b27e259)

![image](https://github.com/user-attachments/assets/3040fcbe-b3ba-42e8-9ae2-c555af4d644e)


- PASO 2: Guardamos la información en archivos de texto, usando como ejemplo todas las señales del locutor **SES005**
  ![image](https://github.com/user-attachments/assets/ae8e127b-7459-4e96-908c-c25a3f6622fd)

- PASO 3: Ejecutando el siguiente script de phyton, generamos las gráficas

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
import matplotlib.pyplot as plt
import numpy as np

#Gráfica LP
graph_lp = np.loadtxt('lp.txt')
plt.figure(1)
plt.plot(graph_lp[:, 0], graph_lp[:, 1], '.', color='red')
plt.grid(True)
plt.xlabel('coef 2')
plt.ylabel('coef 3')
plt.title('LP')

#Gráfica LPCC
graph_lpcc = np.loadtxt('lpcc.txt')
plt.figure(2)
plt.plot(graph_lpcc[:, 0], graph_lpcc[:, 1], '.', color='green')
plt.grid(True)
plt.xlabel('coef 2')
plt.ylabel('coef 3')
plt.title('LPCC')

#Gráfica MFCC
graph_mfcc = np.loadtxt('mfcc.txt')
plt.figure(3)
plt.plot(graph_mfcc[:, 0], graph_mfcc[:, 1], '.', color='blue')
plt.grid(True)
plt.xlabel('coef 2')
plt.ylabel('coef 3')
plt.title('MFCC')

plt.show()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

→ Parametrización **LP**:
![LP_caract](https://github.com/user-attachments/assets/759c4c08-95bc-4502-a447-27ec9d32d20a)


→ Parametrización **LPCC**:
![LPCC_caract](https://github.com/user-attachments/assets/16969c0b-2cad-4cc7-ac71-d00adcdf931a)



→ Parametrización **MFCC**:
![MFCC_caract](https://github.com/user-attachments/assets/022cab77-6a8f-4a8d-958d-0897fd209d69)


  + ¿Cuál de ellas le parece que contiene más información?

Los coeficientes LPCC son una transformación cepstral de los LPC. Esta transformación reduce la correlación entre las características y los LPCC tienden a contener más información relevante y diferenciada, ya que capturan tanto la envolvente espectral como sus variaciones de una manera más incorrelada.

Los coeficientes cepstrales en la escala Mel están diseñados explícitamente para reducir las correlaciones entre sí después de una transformación en el dominio de frecuencias. Generalmente, tienen los coeficientes menos correlacionados entre estas tres técnicas.

En conclusión, la gráfica asociada con los MFCC (última gráfica) contiene más información, ya que los coeficientes están más inorrelados en comparación con los LP y LPCC.

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

![image](https://github.com/user-attachments/assets/93437e09-5ab7-4b86-9ff1-d5a2f38506b4)




  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |  -0.72    |   0.22   |   0.15   |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
  
Los valores obtenidos para ρx[2,3] nos indican el nivel de correlación entre los coeficientes 2 y 3, donde el que tiene una mayor correlación es aquel que tiene un valor más cercano al 1. 
De la tabla superior, vemos que, en valor absoluto, para LP obtenemos un valor más cercano a 1, por lo que éste aporta menos información. 
Por otro lado, LPCC y MFCC son menores y están más cerca del 0, por lo que sus coeficientes son más incorrelados entre sí y, de este modo, podemos decir que aportan más información. Siendo aún más precisas, podemos ver como los coeficientes MFCC son ligeramente más incorrelados que los de LPCC. Dicho esto, los resultados pearson concuerdan con los resultados gráficos obtenidos anteriormente.


- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

**Para LPCC:** Cada orden 2 equivale a 1 formante; los dos primeros formantes son esenciales, el 3ro añade naturalidad y los demás son características del locutor. Si el orden es muy elevado -> Info que no es relevante para el reconocimiento. Si quiero 5-6 resonancias, con orden 10, 12, 14 o incluso 16 es suficiente. En nuestro caso hemos usado LPCC de orden 30 porque daban mejores resultados.

**Para MFCC**: hemos usado una frecuencia de muestreo de 8Khz, 16 coeficientes y entre 24 y 40 filtros.

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.

![image](https://github.com/user-attachments/assets/2c50268b-eaf5-4da8-b6b3-a5d3369fe3b1)



- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

![image](https://github.com/user-attachments/assets/bf02da2a-51ba-4285-8d67-60d2b93e2d1b)






### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

![image](https://github.com/user-attachments/assets/d1766be5-175e-4dd7-b6a4-3fe926c38d25)

  | |LP|LPCC|MFCC|
  |:-----|:-----:|:----:|:------:|
  | Error rate|8.79%|1.40%|0.89%|




### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.


  ![image](https://github.com/user-attachments/assets/2b3b7ef5-51f6-4449-bdc4-461640ee4508)

  |                        | LP      | LPCC   | MFCC   |
  |------------------------|:-------:|:------:|:------:|
  |Umbral óptimo           | 0.2178   |  -0.009875  |  0.3996|
  | Misses                 | 85/250  | 16/250 | 23/250 |
  | Falsa alarma           | 15/1000 | 3/1000 | 3/1000 |
  | Cost detection         | 47.5    | 9.1     | 11.9   |

  
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
