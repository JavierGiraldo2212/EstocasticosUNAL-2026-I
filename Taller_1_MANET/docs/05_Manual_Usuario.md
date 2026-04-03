# 05. Manual de Usuario: Ejecución de Escenarios MANET

## 1. Requisitos Previos
El usuario debe contar con un entorno Linux (Ubuntu) con el simulador NS-3 (versión 3.43) compilado e instalado en su sistema.

## 2. Ejecución del Simulador
El script de simulación cuenta con parámetros de línea de comandos dinámicos, lo que permite modificar las variables del experimento sin necesidad de alterar o recompilar el código fuente en C++. 

Para ejecutar los escenarios, abra una terminal, navegue hasta el directorio principal de NS-3 y utilice el comando de ejecución estándar, variando el parámetro `--velocityL2` (velocidad de los clústeres de nivel 2 expresada en m/s).

## 3. Guía de Ejecución para los 3 Escenarios de Prueba

* **Escenario 1 (Control - Baja Movilidad):**
    Simula clústeres moviéndose a velocidad peatonal (2 m/s).
    `./ns3 run "Taller1/manet_jerarquica --velocityL2=2.0"`

* **Escenario 2 (Movilidad Moderada):**
    Simula clústeres moviéndose a velocidad vehicular urbana (15 m/s).
    `./ns3 run "Taller1/manet_jerarquica --velocityL2=15.0"`

* **Escenario 3 (Estrés - Alta Movilidad):**
    Simula clústeres desplazándose a alta velocidad (30 m/s) para evaluar la ruptura de enlaces.
    `./ns3 run "Taller1/manet_jerarquica --velocityL2=30.0"`

## 4. Resultados Generados
Independientemente del escenario ejecutado, el simulador generará automáticamente un archivo en el directorio raíz de NS-3 llamado `manet-metrics.xml`. Este archivo contiene todos los datos recolectados durante la simulación y puede ser procesado posteriormente mediante scripts de Python para generar gráficas de rendimiento.