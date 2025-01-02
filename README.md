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

Este script tiene como objetivo realizar una extracción de características LPC (Linear Predictive Coding) a partir de un archivo de audio en formato WAV. Este proceso utiliza herramientas de la biblioteca SPTK (Speech Signal Processing Toolkit) y se realiza mediante una canalización (pipeline) de comandos.

→ **Comando SOX**: Convierte el archivo de entrada en formato WAV ($inputfile) a un flujo de datos de audio sin procesar en formato RAW.

-t raw:  formato de salida será RAW (datos binarios sin encabezado).<br>
-e signed: datos de audio serán enteros con signo.<br>
-b 16: cada muestra de audio tiene un tamaño de 16 bits (profundidad).<br>
-: la salida será enviada al flujo estándar (stdout), para que pueda ser utilizada en la canalización.

→ **Comando $X2X**: Convierte los datos binarios RAW generados por sox en números de coma flotante (formato requerido para el procesamiento posterior).  (+sf -> single-precision floating-point)

→ **Comando $FRAME**: Divide los datos de audio en frames de longitud constante, permitiendo que cada uno sea procesado independientemente.

-l 240: Define la longitud de cada frame como 240 muestras (30 ms con una frecuencia de muestreo de 8 kHz).<br>
-p 80: Establece un desplazamiento (overlap) entre frames de 80 muestras (10 ms).<br>

→ **Comando $WINDOW**: Se enventana la señal con los parámetros especificados a continuación.

-l 240: longitud de la señal de entrada (240 muestras).<br>
-L 240: longitud de la ventana (también 240 muestras).<br>

→ **Comando $LPC**: Realiza el análisis LPC sobre cada frame para obtener los coeficientes lineales predictivos. Estos coeficientes representan de forma compacta el espectro del audio.

-l 240: Longitud de la señal de entrada (240 muestras por frame).<br>
-m $lpc_order: Orden del análisis LPC (número de coeficientes).<br>

El script convierte un archivo WAV en un archivo LPC comprimido, que contiene los coeficientes lineales predictivos organizados en una matriz con encabezado.

- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 49 a 55 del script `wav2lp.sh`).
  
Primero se determina el número de columnas del fichero de salida y el valor lpc_order que representa el orden del análisis LPC. Luego, se suma 1 para incluir el coeficiente de ganancia (gain) en la primera columna.

En la siguiente linea se utiliza el comando $X2X +fa para convertir los datos LPC almacenados en formato binario a texto flotante (ASCII). A demás, los datos se leen desde el archivo $base.lp, que contiene los coeficientes LPC generados por SPTK.<br>
wc -l cuenta el número de líneas (valores) en el archivo convertido.
Posteriormente, se divide el número total de valores entre ncol (número de columnas) para calcular el número de filas. Esta división garantiza que cada fila tenga exactamente ncol valores.

El formato fmatrix requiere un encabezado con el número de filas y columnas, por eso el script añade esta información en el fichero para cumplir con el formato requerido.

  * ¿Por qué es más conveniente el formato *fmatrix* que el SPTK?

El formato fmatrix es más conveniente que el formato nativo de SPTK por varias razones: <br>
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
  + ¿Cuál de ellas le parece que contiene más información?

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |      |      |      |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.

- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
