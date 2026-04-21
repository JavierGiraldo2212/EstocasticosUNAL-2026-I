# Taller 1: Simulación de MANET Jerárquica con Movilidad Dual

## Objetivo de la Indagación
Evaluar, mediante el método científico, el impacto de la velocidad de desplazamiento de los clústeres troncales (Nivel 2) en el Throughput, la Latencia y el Packet Delivery Ratio (PDR) de los nodos hoja (Nivel 1) en una red MANET jerárquica, contrastando el rendimiento de un protocolo de enrutamiento reactivo (AODV) frente a uno proactivo (OLSR).

## Arquitectura del Sistema
El modelo implementa una topología de red de dos niveles:
* **Nivel 1 (Hojas):** 3 clústeres de 5 nodos cada uno, con movilidad local aleatoria (`RandomWalk2dMobilityModel`).
* **Nivel 2 (Backbone):** 2 clústeres de 3 nodos cada uno, que actúan como puente inter-clúster, con movilidad grupal direccional coordinada (`GaussMarkovMobilityModel`).

## Estructura de Carpetas
El proyecto se organiza de la siguiente manera:

```text
Taller_1_MANET/
├── README.md                           # Este archivo con información general del taller
├── docs/                               # Documentación del proyecto (Entregables)
│   ├── 01_Marco_Teorico.md             # Marco teórico sobre MANET y protocolos de enrutamiento
│   ├── 02_Descripcion_Justificacion.md # Indagación científica e hipótesis
│   ├── 03_Diseno_Solucion.md           # Diseño de la arquitectura y pseudocódigo
│   ├── 04_Manual_Tecnico.md            # Especificaciones de software y clases de NS-3
│   ├── 05_Manual_Usuario.md            # Guía de ejecución por consola
│   └── 06_Experimentacion_Resultados.md# Análisis comparativo y conclusiones (AODV vs OLSR)
├── design/                             # Diagramas y esquemas del sistema
│   ├── topologia.puml                  # Diagrama de la topología jerárquica
│   └── flujo_simulacion.puml           # Diagrama de flujo del algoritmo y enrutamiento dinámico
├── src/                                # Código fuente
│   └── manet_jerarquica.cc             # Programa principal de simulación en C++
└── experiments/                        # Scripts de análisis
    └── parse_metrics.py                # Extractor de métricas para la comparativa de los 6 escenarios
```

## Descripción de Componentes
* **docs**: Contiene toda la documentación obligatoria en formato Markdown, estructurada secuencialmente desde la conceptualización teórica hasta la validación empírica y extracción de resultados comparativos.
* **design**: Diagramas en formato PlantUML que especifican gráficamente la topología de la red y la inyección condicional de la pila de red.
* **src**: Código fuente modular implementado en C++ para NS-3.43. Permite la selección dinámica de la velocidad y del protocolo de enrutamiento (AODV u OLSR) vía línea de comandos.
* **experiments**: Scripts en Python para la automatización del análisis. Incluye `ai_controller.py` para la optimización de parámetros de red mediante inteligencia artificial (ns3-ai), y `parse_metrics.py` para leer y analizar simultáneamente los archivos XML generados por FlowMonitor, consolidando las métricas de rendimiento de la comparativa.

## Instrucciones de Ejecución
Este proyecto está diseñado para compilarse dentro del entorno de NS-3. Se recomienda crear un enlace simbólico desde el directorio `scratch` de NS-3 hacia la carpeta `src` de este directorio.

**1. Generar enlace simbólico:**
```bash
ln -s /ruta/a/este/repo/Taller_1_MANET/src /ruta/a/ns-allinone-3.43/ns-3.43/scratch/Taller1
```

**2. Ejecutar la simulación (Ejemplo comparativo a 15 m/s):**
Navegue al directorio raíz de NS-3 y ejecute el simulador especificando la velocidad y el protocolo. Renombre el archivo de salida inmediatamente para la comparativa:

Para AODV:
```bash
./ns3 run "Taller1/manet_jerarquica --velocityL2=15.0 --protocol=AODV"
mv metrics_AODV.xml metrics_AODV_15.xml
```

Para OLSR:
```bash
./ns3 run "Taller1/manet_jerarquica --velocityL2=15.0 --protocol=OLSR"
mv metrics_OLSR.xml metrics_OLSR_15.xml
```

**3. Análisis de Resultados:**
Una vez generados los archivos XML para los escenarios deseados, ejecute el script de análisis para calcular el PDR, Latencia y Throughput:
```bash
python experiments/parse_metrics.py
```
