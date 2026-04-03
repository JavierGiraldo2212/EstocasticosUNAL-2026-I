# 01. Marco Teorico

## 1. Introducción a las Redes MANET (Mobile Ad Hoc Networks)
Las redes móviles ad hoc (MANET) son sistemas dinámicos de comunicaciones inalámbricas que operan sin una infraestructura física o administración centralizada preexistente. En estos entornos, cada nodo actúa simultáneamente como terminal y como enrutador, retransmitiendo paquetes de forma cooperativa para establecer la comunicación "salto a salto" (multi-hop). Su capacidad de autoconfiguración las hace ideales para modelar sistemas complejos de telecomunicaciones bajo la óptica de los modelos estocásticos.

## 2. Topologías Jerárquicas y Segmentación en Clústeres
Para garantizar la escalabilidad y mitigar la saturación por mensajes de control en redes densas, el enrutamiento plano suele ser insuficiente. Como solución, se emplean arquitecturas jerárquicas:
* **Clústeres de Primer Nivel (Leaf Clusters):** Agrupaciones de nodos que se comunican localmente y reportan a un nodo cabecera (Cluster Head).
* **Clústeres de Segundo Nivel (Backbone Clusters):** Estructuras superiores que enlazan los clústeres de primer nivel, actuando como una red troncal para el tráfico inter-clúster.
* **Segmentación:** La simulación de estos entornos permite combinar tecnologías, como enlaces mixtos (LAN cableadas y redes inalámbricas), para organizar de forma eficiente el flujo de información y reducir el *overhead* de enrutamiento.

## 3. Dinámica y Modelos de Movilidad
En el diseño y simulación de redes MANET, la movilidad es la principal fuente de incertidumbre (comportamiento estocástico) y determina el desempeño del protocolo de enrutamiento.
* **Movilidad a Nivel de Nodo:** Define el desplazamiento individual y semi-aleatorio de cada dispositivo dentro de su respectivo clúster.
* **Movilidad a Nivel de Clúster (Group Mobility):** Representa el movimiento coordinado de todo el grupo o subred siguiendo un vector o nodo líder, aplicable en escenarios tácticos o vehiculares.
* **Impacto Estocástico:** Los patrones de movimiento afectan variables aleatorias como la duración del enlace (Link Duration) y la probabilidad de colisión de paquetes.

## 4. Herramientas Computacionales: NS-3 y ns3-ai
La validación de estas arquitecturas requiere herramientas especializadas de simulación de eventos discretos. 
* **Simulador NS-3:** Entorno modular estándar en la industria e investigación que permite modelar con alta fidelidad las capas físicas y MAC, así como diversos protocolos de red.
* **Módulo ns3-ai:** Extensión que reemplaza a arquitecturas previas (como AI Gym) y facilita la integración del simulador con frameworks de Inteligencia Artificial (basados en Python), permitiendo la extracción de datos de telemetría y control de red en tiempo real.
* **Metodología de Experimentación:** Siguiendo los lineamientos operativos para tareas automatizadas, la evaluación de estos modelos requiere la definición de un marco teórico riguroso y la ejecución y documentación de al menos tres (3) escenarios de prueba para contrastar el comportamiento del sistema.

## 5. Protocolos de Enrutamiento: Paradigmas Reactivo vs Proactivo
El enrutamiento en MANET se clasifica principalmente en dos enfoques, los cuales reaccionan distinto frente a la estocasticidad de la movilidad:
* **Protocolos Reactivos (ej. AODV):** Descubren rutas "bajo demanda" mediante inundación de mensajes de búsqueda. Tienen menor *overhead* en redes estáticas, pero introducen alta latencia durante el descubrimiento de la ruta.
* **Protocolos Proactivos (ej. OLSR):** Mantienen tablas de enrutamiento actualizadas continuamente intercambiando información de estado de enlace (ej. mensajes *Hello* e información de topología mediante nodos MPR). Ofrecen latencia casi nula, pero sufren de un alto *overhead* de control y posibles rutas caducadas si la movilidad es extrema.

## 6. Modelos de Movilidad y Simulación
En el diseño y simulación, la movilidad dicta el desempeño del enrutamiento.
* **Movilidad de Nodo:** Desplazamiento local de dispositivos (ej. `RandomWalk2dMobilityModel`).
* **Movilidad de Clúster:** Movimiento direccional coordinado de una subred (ej. `GaussMarkovMobilityModel`).
* **Herramientas (NS-3):** Entorno modular que permite modelar con alta fidelidad las capas físicas (802.11) y evaluar el desempeño mediante múltiples escenarios de prueba obligatorios.

## Referencias Bibliográficas
[1] J. E. Ortiz Triviño, "Lineamientos Operativos: Modelos Estocásticos y Simulación en Computación y Comunicaciones," Universidad Nacional de Colombia, Bogotá, 2026.  
[2] H. Zárate Ceballos *et al.*, *Wireless Network Simulation: A Guide using Ad Hoc Networks and the ns-3 Simulator*. Apress, 2021.  
[3] Proyecto NS-3, "Mixed Wired Wireless Example," *ns-3.27 Doxygen*. [En línea]. Disponible: https://www.nsnam.org/  
[4] Laboratorio Dian (HUST), "NS-3 AI Integration Module (ns3-ai)," *GitHub*. [En línea]. Disponible: https://github.com/hust-diangroup/ns3-ai