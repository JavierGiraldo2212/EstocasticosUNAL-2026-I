# 06 Experimentación y Resultados

## 1. Contexto de la Experimentación
Se simularon tres (3) escenarios en NS-3 variando únicamente la velocidad del clúster backbone (Nivel 2) para aislar su efecto sobre el rendimiento de la red. La topología consiste en una MANET jerárquica con tres clústeres en el primer nivel y dos en el segundo. 

Las condiciones generales de la simulación fueron:
* **Área de simulación:** 250x250 metros.
* **Duración:** 100 segundos.
* **Protocolo de enrutamiento:** AODV.
* **Movilidad Nivel 1 (Hojas):** Modelo `RandomWalk2D` con una velocidad constante de 1 m/s.
* **Movilidad Nivel 2 (Backbone):** Modelo `Gauss-Markov` variando la velocidad según el escenario (2 m/s, 15 m/s y 30 m/s).

## 2. Resultados Obtenidos
Las métricas fueron recolectadas mediante la herramienta `FlowMonitor` y evidencian el comportamiento de la red ante diferentes niveles de estrés por movilidad.

* **Escenario 1 (Control - 2 m/s):**
  * **Paquetes Transmitidos:** 1037 | **Paquetes Recibidos:** 129
  * **Packet Delivery Ratio (PDR):** 12.44% | **Packet Loss Ratio (PLR):** 44.87%
  * **Throughput:** 9.727 Kbps
  * **Latencia Media:** 11.78 ms | **Jitter Medio:** 3.19 ms

* **Escenario 2 (Moderado - 15 m/s):**
  * **Paquetes Transmitidos:** 1050 | **Paquetes Recibidos:** 137
  * **Packet Delivery Ratio (PDR):** 13.05% | **Packet Loss Ratio (PLR):** 44.71%
  * **Throughput:** 8.545 Kbps
  * **Latencia Media:** 178.02 ms | **Jitter Medio:** 74.53 ms

* **Escenario 3 (Estrés - 30 m/s):**
  * **Paquetes Transmitidos:** 1330 | **Paquetes Recibidos:** 522
  * **Packet Delivery Ratio (PDR):** 39.25% | **Packet Loss Ratio (PLR):** 37.65%
  * **Throughput:** 34.094 Kbps
  * **Latencia Media:** 29.74 ms | **Jitter Medio:** 7.62 ms

## 3. Análisis de Resultados
Los datos obtenidos demuestran que la velocidad de movimiento de los clústeres backbone tiene un impacto medible y contraintuitivo sobre las métricas de red:

1. **Efecto sobre el PDR y PLR:** El escenario con el mejor desempeño en entrega de paquetes fue el Escenario 3 (30 m/s) alcanzando un PDR de 39.25%, mientras que el peor fue el Escenario 1 de control (2 m/s) con apenas un 12.44%. Aunque a mayor velocidad el protocolo AODV debe recalcular rutas con mayor frecuencia (aumentando la probabilidad de pérdida por ruptura de enlaces), el aumento de movilidad extrema parece favorecer el encuentro oportunista entre clústeres.
2. **Comportamiento del Throughput:** De manera similar, el escenario de mayor rendimiento general fue el de 30 m/s (34.094 Kbps).En los escenarios de menor velocidad, la degradación se debe a prolongados períodos de desconexión mientras el enrutamiento reactivo intenta redescubrir las rutas.
3. **Costo temporal de la movilidad (Latencia y Jitter):** El pico de latencia observado en el Escenario 2 (178.02 ms) revela el costo temporal de la movilidad. El incremento drástico en la latencia confirma que el overhead de los mensajes RREQ/RREP en AODV crece al aumentar la frecuencia de las rupturas de enlaces antes de estabilizarse.

## 4. Conclusiones y Recomendaciones
* **Robustez y Cuellos de Botella:** AODV logra mantener la conectividad a lo largo de los escenarios, pero su latencia de reconvergencia se convierte en un cuello de botella significativo ante una movilidad moderada-alta.
* **Evaluación de Protocolos Proactivos:** Para escenarios de alto estrés (30 m/s), se recomienda fuertemente evaluar OLSR o un enfoque de enrutamiento híbrido. Esto permitiría mantener un estado proactivo en el backbone mientras se conserva la reactividad en los nodos hoja.
* **Ajustes Topológicos:** Se sugiere aumentar el área de simulación o reducir la densidad de los nodos para suavizar los "efectos de borde" observados en los clústeres de Nivel 2 que se desplazan a altas velocidades.
