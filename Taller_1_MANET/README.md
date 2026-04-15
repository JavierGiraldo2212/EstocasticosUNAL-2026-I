# Taller 1: Simulación de MANET Jerárquica con Movilidad Dual

## Objetivo de la Indagación
Evaluar, mediante el método científico, el impacto de la velocidad de desplazamiento de los clústeres troncales (Nivel 2) en el *Throughput* y el *Packet Delivery Ratio* (PDR) de los nodos hoja (Nivel 1) en una red MANET jerárquica, utilizando el protocolo de enrutamiento AODV.

## Arquitectura del Sistema
El modelo implementa una topología de red de dos niveles:
* **Nivel 1 (Hojas):** 3 clústeres de 5 nodos cada uno, con movilidad local aleatoria (`RandomWalk2dMobilityModel`).
* **Nivel 2 (Backbone):** 2 clústeres de 3 nodos cada uno, que actúan como puente inter-clúster, con movilidad grupal direccional coordinada (`GaussMarkovMobilityModel`).

## Estructura de Carpetas
El proyecto se organiza de la siguiente manera:

```
Taller_1_MANET/
├── README.md                    # Este archivo con información general del taller
├── docs/                        # Documentación del proyecto
│   ├── 01_Marco_Teorico.md     # Marco teórico sobre MANET y modelos estocásticos
│   ├── 02_Descripcion_Problema.md
│   ├── 03_Manual_Usuario.md
│   ├── 04_Manual_Tecnico.md
│   └── 05_Analisis_Resultados.md
├── design/                      # Diagramas y esquemas del sistema
│   ├── topologia_red.puml      # Diagrama de la topología jerárquica
│   └── flujo_simulacion.puml   # Diagrama de flujo del algoritmo
├── src/                         # Código fuente
│   └── manet_jerarquica.cc     # Programa principal de simulación en C++
└── experiments/                 # Scripts de análisis
    └── parse_metrics.py        # Extractor de métricas desde XML
```

## Descripción de Componentes
* **docs**: Contiene toda la documentación en formato Markdown, incluyendo marco teórico, descripción del problema, manuales de usuario y técnico, así como el análisis de resultados experimentales.
* **design**: Diagramas en formato PlantUML que especifican la topología de la red jerárquica y el flujo de la simulación.
* **src**: Código fuente completo implementado en C++ utilizando el framework NS-3, que define la arquitectura de dos niveles, los modelos de movilidad y el protocolo AODV.
* **experiments**: Scripts en Python para procesar automáticamente los archivos XML generados por FlowMonitor y extraer las métricas de desempeño (Throughput y PDR).

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
Los datos se exportan a `manet-metrics.xml`. Para procesarlos, utilizar el script de extracción:
```bash
python experiments/parse_metrics.py
```
