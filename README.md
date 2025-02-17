

# Proyecto de Detección y Corrección de Errores

Este proyecto implementa un sistema de detección y corrección de errores utilizando el código de Hamming en el emisor y el checksum de Fletcher en el receptor. Se utiliza C++ para el emisor y Python para el receptor, con comunicación a través de sockets TCP.

## Requisitos

- **Para el Emisor:**
  - Compilador de C++ (por ejemplo, `g++`)
  - Bibliotecas estándar de C++ (no hay dependencias externas)

- **Para el Receptor:**
  - Python 3
  - Bibliotecas `numpy` y `matplotlib` (pueden instalarse usando `pip install numpy matplotlib`)

## Código del Emisor

El código del emisor está escrito en C++ y realiza las siguientes funciones:
1. **Codificación de Hamming:** Codifica mensajes ASCII en binario y aplica el código de Hamming para detectar y corregir errores.
2. **Aplicación de Ruido:** Introduce errores en el mensaje codificado con una probabilidad específica.
3. **Envío de Mensajes:** Envía el mensaje codificado (con ruido) a un servidor usando sockets TCP.

### Cómo Ejecutar el Emisor

1. **Compila el código C++:**
   ```sh
   g++ -o hammingCorrection hammingCorrection.cpp
   g++ -o hammingCorrectionTest hammingCorrectionTest.cpp
   ```

2. **Ejecuta el programa:**
   ```sh
   ./hammingCorrectionTest
   ./hammingCorrection
   ```

3. **Introduce un mensaje ASCII cuando se te solicite.**

## Código del Receptor

El código del receptor está escrito en Python y realiza las siguientes funciones:
1. **Decodificación de Hamming:** Detecta y corrige errores en el mensaje recibido usando el código de Hamming.
2. **Cálculo del Checksum de Fletcher:** Calcula y verifica el checksum para detectar errores.
3. **Visualización de Resultados:** Genera gráficos sobre la distribución de errores, errores acumulados y errores de checksum.

### Cómo Ejecutar el Receptor

1. **Asegúrate de tener las bibliotecas necesarias:**
   ```sh
   pip install numpy matplotlib
   ```

2. **Ejecuta el programa:**
   ```sh
   python receptor_test.py
   python receptor.py
   ```

3. **El receptor estará esperando conexiones en el puerto 12345.**

## Cómo Funciona

1. **El Emisor:**
   - Codifica un mensaje ASCII en binario.
   - Aplica el código de Hamming para la corrección de errores.
   - Introduce errores en el mensaje codificado con una probabilidad especificada.
   - Envía el mensaje con ruido al servidor (receptor) usando sockets TCP.

2. **El Receptor:**
   - Escucha conexiones entrantes en el puerto 12345.
   - Recibe el mensaje y aplica el código de Hamming para detectar y corregir errores.
   - Calcula el checksum de Fletcher para verificar la integridad del mensaje.
   - Genera gráficos sobre el desempeño de los algoritmos de detección y corrección de errores.

## Resultados Esperados

- **Gráficos Generados:**
  - Distribución de errores por posición de bit.
  - Errores acumulados a lo largo del tiempo.
  - Errores de checksum a lo largo del tiempo.

## Conclusiones

- El código de Hamming es ideal para corrección de errores en situaciones donde la tasa de errores es baja a moderada. Es efectivo para corregir errores en mensajes pero puede ser menos eficiente cuando la tasa de errores es alta.
- El checksum de Fletcher es más flexible para tasas de error más altas y proporciona una detección de errores rápida con menos sobrecarga, aunque no puede corregir errores.

## Referencias Bibliográficas

- Wright, G. (2022, July 11). What is Hamming code and how does it work?. WhatIs. [Enlace](https://www.techtarget.com/whatis/definition/Hamming-code#:~:text=Hamming%20code%20is%20an%20error,after%20its%20inventor%2C%20Richard%20W.)
- Fletcher’s checksum. Tutorialspoint. [Enlace](https://www.tutorialspoint.com/fletcher-s-checksum)
- PU5EPX, E. P. (n.d.). Error detection and correction. EPx. [Enlace](https://epxx.co/artigos/edc_en.html)
