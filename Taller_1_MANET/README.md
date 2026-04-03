# Taller 1: Simulación de MANET Jerárquica con Movilidad Dual

## Objetivo de la Indagación
Evaluar, mediante el método científico, el impacto de la velocidad de desplazamiento de los clústeres troncales (Nivel 2) en el *Throughput* y el *Packet Delivery Ratio* (PDR) de los nodos hoja (Nivel 1) en una red MANET jerárquica, utilizando el protocolo de enrutamiento AODV.

## Arquitectura del Sistema
El modelo implementa una topología de red de dos niveles:
* **Nivel 1 (Hojas):** 3 clústeres de 5 nodos cada uno, con movilidad local aleatoria (`RandomWalk2dMobilityModel`).
* **Nivel 2 (Backbone):** 2 clústeres de 3 nodos cada uno, que actúan como puente inter-clúster, con movilidad grupal direccional coordinada (`GaussMarkovMobilityModel`).

## Estructura de Entregables
Cumpliendo con los lineamientos operativos del curso, esta carpeta contiene los siguientes entregables:
* `/docs`: Archivos en formato Markdown/PDF que incluyen el Marco Teórico, Descripción del problema, Manual de Usuario, Manual Técnico y Análisis de Resultados.
* `/design`: Diagramas de flujo y topología de red desarrollados en PlantUML.
* `/src`: Código fuente completo en C++ (`manet_jerarquica.cc`).
* `/experiments`: Scripts en Python para la extracción automática de métricas desde archivos XML generados por `FlowMonitor`.

## Instrucciones de Ejecución
Este proyecto está diseñado para compilarse dentro del entorno de NS-3. Se recomienda crear un enlace simbólico desde el directorio `scratch` de NS-3 hacia la carpeta `src` de este directorio.

**1. Generar enlace simbólico:**
```bash
ln -s /ruta/a/este/repo/Taller_1_MANET/src /ruta/a/ns-allinone-3.43/ns-3.43/scratch/Taller1
```

**2. Ejecutar la simulación (Escenario de ejemplo a 15 m/s):**
Navegue al directorio de NS-3 y ejecute:
```bash
./ns3 run "Taller1/manet_jerarquica --velocityL2=15.0"
```

**3. Análisis de Resultados:**
Los datos se exportan a `manet-metrics.xml`. Para procesarlos, utilice el script de extracción:
```bash
python experiments/parse_metrics.py
```
