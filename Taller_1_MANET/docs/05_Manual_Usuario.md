# 05. Manual de Usuario: Ejecución de Escenarios MANET

## 1. Requisitos Previos
El usuario debe contar con un entorno Linux (Ubuntu) con el simulador NS-3 (versión 3.43) compilado e instalado en su sistema. Adicionalmente, se recomienda contar con Python 3 para ejecutar los scripts de extracción y análisis de métricas.

## 2. Ejecución del Simulador
El script de simulación cuenta con parámetros de línea de comandos dinámicos, lo que permite modificar las variables del experimento sin necesidad de alterar o recompilar el código fuente en C++. 

Para ejecutar los escenarios, abra una terminal, navegue hasta el directorio principal de NS-3 y utilice el comando de ejecución estándar, variando dos parámetros clave: 
* `--velocityL2`: Velocidad global de los clústeres de nivel 2 expresada en m/s.
* `--protocol`: Protocolo de enrutamiento a evaluar. Soporta los valores `AODV` (reactivo) u `OLSR` (proactivo).

## 3. Guía de Ejecución para la Comparativa de 6 Escenarios

Para lograr una comparativa precisa, es fundamental ejecutar el simulador y renombrar el archivo de salida inmediatamente para evitar sobrescrituras.

**A. Pruebas con Protocolo Reactivo (AODV):**
* **Escenario 1 (Control - Baja Movilidad):**
  `./ns3 run "Taller1/manet_jerarquica --velocityL2=2.0 --protocol=AODV"`
  `mv metrics_AODV.xml metrics_AODV_2.xml`

* **Escenario 2 (Movilidad Moderada):**
  `./ns3 run "Taller1/manet_jerarquica --velocityL2=15.0 --protocol=AODV"`
  `mv metrics_AODV.xml metrics_AODV_15.xml`

* **Escenario 3 (Estrés - Alta Movilidad):**
  `./ns3 run "Taller1/manet_jerarquica --velocityL2=30.0 --protocol=AODV"`
  `mv metrics_AODV.xml metrics_AODV_30.xml`

**B. Pruebas con Protocolo Proactivo (OLSR):**
* **Escenario 1 (Control - Baja Movilidad):**
  `./ns3 run "Taller1/manet_jerarquica --velocityL2=2.0 --protocol=OLSR"`
  `mv metrics_OLSR.xml metrics_OLSR_2.xml`

* **Escenario 2 (Movilidad Moderada):**
  `./ns3 run "Taller1/manet_jerarquica --velocityL2=15.0 --protocol=OLSR"`
  `mv metrics_OLSR.xml metrics_OLSR_15.xml`

* **Escenario 3 (Estrés - Alta Movilidad):**
  `./ns3 run "Taller1/manet_jerarquica --velocityL2=30.0 --protocol=OLSR"`
  `mv metrics_OLSR.xml metrics_OLSR_30.xml`

## 4. Resultados Generados
Dependiendo del protocolo seleccionado, el simulador generará automáticamente un archivo en el directorio raíz de NS-3 llamado `metrics_AODV.xml` o `metrics_OLSR.xml`. 

Una vez generados y renombrados los seis (6) archivos según la guía anterior, estos pueden ser procesados mediante el script `parse_metrics.py` (ubicado en la carpeta `experiments` del repositorio). Este script de Python se encarga de analizar los flujos detectados y calcular automáticamente el Throughput, la Latencia Media y el Packet Delivery Ratio (PDR) de toda la comparativa.