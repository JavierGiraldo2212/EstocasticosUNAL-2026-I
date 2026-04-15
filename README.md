# Modelos Estocásticos y Simulación en Computación y Comunicaciones

**Universidad Nacional de Colombia - Sede Bogotá** **Semestre:** 2026-01  
**Profesor:** Jorge Eduardo Ortiz Triviño  
**Autores:** 
- Javier Santiago Giraldo Jiménez  

##  Descripción del Repositorio
Este repositorio contiene el código fuente, la documentación técnica y los resultados de experimentación de los trabajos prácticos desarrollados para la asignatura "Modelos Estocásticos y Simulación en Computación y Comunicaciones". El enfoque principal es el uso del simulador de eventos discretos **NS-3** (versión 3.43) y la integración de herramientas de inteligencia artificial mediante **ns3-ai**.

## Estructura del Repositorio
El repositorio está estructurado de acuerdo con las actividades evaluativas del curso:

*  **Taller_1_MANET/**: Simulación de una Red Ad Hoc Móvil (MANET) jerárquica con movilidad dual grupal/nodal.
*  **Taller_2/**: *(Por definir en el calendario académico)*.
*  **Proyecto_Final/**: Desarrollo de simulación estocástica de alta complejidad como trabajo de cierre del semestre.

##  Herramientas y Dependencias
* **Sistema Operativo:** Ubuntu Linux.
* **Simulador Core:** NS-3.43.
* **Lenguajes:** C++ (Core), Python 3.11 (Análisis y ns3-ai).
* **Dependencias Extra:** `ns3-ai`, `FlowMonitor`, Entorno virtual Conda.

##  Estructura del proyecto
EstocasticosUNAL-2026-I/
├── .vscode/
│   └── c_cpp_properties.json
├── Taller_1_MANET/
│   ├── design/
│   │   ├── flujo_simulacion.png
│   │   ├── flujo_simulacion.puml
│   │   ├── topologia.png
│   │   └── topologia.puml
│   ├── docs/
│   │   ├── 01_Marco_Teorico.md
│   │   ├── 02_Descripcion_Justificacion.md
│   │   ├── 03_Diseno_Solucion.md
│   │   ├── 04_Manual_Tecnico.md
│   │   ├── 05_Manual_Usuario.md
│   │   └── 06_Experimentacion_Resultados.md
│   ├── experiments/
│   │   ├── fig1_panel_barras.png
│   │   ├── fig2_lineas_velocidad.png
│   │   ├── fig3_radar.png
│   │   ├── manet_reporte.pdf
│   │   ├── manet_resultados.csv
│   │   └── parse_metrics.py
│   ├── src/
│   │   └── manet_jerarquica.cc
│   └── README.md
├── .gitignore
├── metrics_escenario_1.xml
├── metrics_escenario_2.xml
├── metrics_escenario_3.xml
└── README.md
---
*Para instrucciones específicas de compilación y ejecución, por favor consulte el `README.md` individual dentro de la carpeta de cada trabajo.*
