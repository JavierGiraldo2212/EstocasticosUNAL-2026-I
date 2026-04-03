# 06 Experimentacion Resultados

## 1. Contexto de la Experimentación
Se ejecutaron tres (3) escenarios de prueba variando la velocidad global de los clústeres troncales (Nivel 2) bajo un modelo de movilidad Gauss-Markov, manteniendo a los nodos hoja (Nivel 1) con un movimiento local aleatorio (`RandomWalk2d`). Las simulaciones tuvieron una duración de 100 segundos en un área acotada de 250x250 metros. Las métricas fueron recolectadas y exportadas mediante `FlowMonitor`.

## 2. Resultados Obtenidos

* **Escenario 1 (Control - 2 m/s):**
  * Paquetes Transmitidos: 960 | Paquetes Recibidos: 0
  * Packet Delivery Ratio (PDR): 0.00 %
  * Throughput Global: 0.00 Kbps | Latencia Media: 0.00 ms

* **Escenario 2 (Moderado - 15 m/s):**
  * Paquetes Transmitidos: 990 | Paquetes Recibidos: 433
  * Packet Delivery Ratio (PDR): 43.74 %
  * Throughput Global: 34.11 Kbps | Latencia Media: 110.708 ms

* **Escenario 3 (Estrés - 30 m/s):**
  * Paquetes Transmitidos: 1001 | Paquetes Recibidos: 255
  * Packet Delivery Ratio (PDR): 25.47 %
  * Throughput Global: 19.04 Kbps | Latencia Media: 161.393 ms

## 3. Análisis y Conclusiones
Los resultados respaldan la indagación científica y revelan comportamientos estocásticos de gran interés:
1. **Degradación por Alta Movilidad:** La transición del Escenario 2 al Escenario 3 confirma la hipótesis inicial. Al duplicar la velocidad de los clústeres *backbone* (de 15 a 30 m/s), el PDR se redujo drásticamente (del ~43% al ~25%) y la latencia aumentó un 45%. Esto evidencia que el enrutamiento reactivo AODV sufre de excesivo *overhead* y tiempos muertos tratando de reparar enlaces rotos constantemente.
2. **El fenómeno de Partición Estática (Escenario 1):** El nulo rendimiento a baja velocidad (2 m/s) ilustra un problema clásico en redes MANET dispersas. Debido a la topología inicial aleatoria, el origen y destino quedaron aislados (fuera del rango de ~100m del estándar 802.11g). Al tener baja movilidad, la partición de la red se mantuvo durante toda la simulación. Irónicamente, el aumento de velocidad en los Escenarios 2 y 3 actuó como un mecanismo de enrutamiento oportunista, permitiendo a los nodos acercarse y entregar paquetes.

## 4. Recomendaciones
Para mitigar la pérdida de rendimiento en MANET jerárquicas con alta movilidad, se recomienda evaluar en simulaciones futuras la implementación de protocolos proactivos o híbridos adaptados a clústeres. Asimismo, para solucionar el aislamiento de nodos lentos, se sugiere incrementar la densidad de los clústeres troncales o emplear tecnologías de capa física con mayor rango de cobertura.