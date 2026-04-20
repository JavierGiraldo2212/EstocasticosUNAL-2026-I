# 06. Experimentación, Resultados y Análisis

## 1. Contexto de la Experimentación
Para dotar al estudio de un mayor rigor científico, se amplió el diseño experimental para realizar una comparativa de protocolos de enrutamiento. Se ejecutaron seis (6) escenarios de prueba cruzando tres velocidades para evaluar un protocolo reactivo (AODV) frente a uno proactivo (OLSR). 

Se varió la velocidad global de los clústeres troncales (Nivel 2) bajo un modelo de movilidad Gauss-Markov, manteniendo a los nodos hoja (Nivel 1) con un movimiento local aleatorio (`RandomWalk2d`). Las simulaciones tuvieron una duración de 100 segundos en un área acotada de 250x250 metros. Las métricas fueron recolectadas y exportadas dinámicamente mediante `FlowMonitor`.

## 2. Resultados Obtenidos

A continuación, se presenta la consolidación de las métricas extraídas para ambos protocolos bajo los tres escenarios de estrés por movilidad:

| Protocolo | Escenario (Velocidad) | Paquetes TX | Paquetes RX | PDR (%) | Throughput (Kbps) | Latencia Media (ms) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **AODV** | Escenario 1 (2 m/s) | 960 | 0 | 0.00 % | 0.00 | 0.000 |
| **AODV** | Escenario 2 (15 m/s) | 990 | 433 | 43.74 % | 34.11 | 110.708 |
| **AODV** | Escenario 3 (30 m/s) | 1001 | 255 | 25.47 % | 19.04 | 161.393 |
| **OLSR** | Escenario 1 (2 m/s) | 0 | 0 | 0.00 % | 0.00 | 0.000 |
| **OLSR** | Escenario 2 (15 m/s) | 362 | 232 | 64.09 % | 19.53 | 0.495 |
| **OLSR** | Escenario 3 (30 m/s) | 255 | 69 | 27.06 % | 5.81 | 0.591 |

## 3. Análisis y Conclusiones
Los resultados respaldan la indagación científica y revelan comportamientos estocásticos de gran interés al contrastar ambos paradigmas:

1. **La Ventaja Proactiva en Latencia:** Como se evidencia en la tabla, OLSR demostró una superioridad abrumadora en los tiempos de entrega, manteniendo la latencia en niveles sub-milisegundo (~0.5 ms) frente a los 110-161 ms de AODV. Esto se debe a que OLSR mantiene tablas de rutas precalculadas; sin embargo, esta misma característica explica por qué OLSR registra menos paquetes transmitidos (TX): si la tabla aún no converge, la aplicación descarta el paquete localmente en lugar de iniciar un costoso proceso de búsqueda en la red como lo hace AODV.
2. **Degradación por Alta Movilidad:** La transición del Escenario 2 al Escenario 3 confirma la hipótesis inicial de estrés para ambos protocolos. Al duplicar la velocidad de los clústeres *backbone* (de 15 a 30 m/s), el PDR de AODV se redujo drásticamente (del 43.74% al 25.47%). OLSR sufrió una caída aún más pronunciada (del 64.09% al 27.06%). Esto evidencia que mientras AODV colapsa por *overhead* tratando de reparar enlaces, OLSR fracasa porque las rupturas topológicas ocurren más rápido de lo que logran propagarse sus mensajes de control, enviando tráfico hacia rutas "fantasma".
3. **El fenómeno de Partición Estática (Escenario 1):** El nulo rendimiento a baja velocidad (2 m/s) en ambos protocolos ilustra un problema clásico en redes MANET dispersas. Debido a la topología inicial aleatoria, el origen y destino quedaron aislados (fuera del rango de ~100m del estándar 802.11g). Al tener baja movilidad, la partición de la red se mantuvo durante toda la simulación. Irónicamente, el aumento de velocidad en los Escenarios 2 y 3 actuó como un mecanismo de enrutamiento oportunista, permitiendo a los nodos acercarse y entregar paquetes.

## 4. Recomendaciones
Para mitigar la pérdida de rendimiento en MANET jerárquicas, la elección del protocolo debe condicionarse al entorno: se recomienda OLSR para aplicaciones sensibles a la latencia en movilidad moderada, y protocolos reactivos o híbridos en escenarios de estrés extremo. 

Asimismo, para solucionar las debilidades observadas en altas velocidades y el aislamiento de nodos lentos, se sugiere para trabajos futuros incrementar la densidad de los clústeres troncales e integrar la librería `ns3-ai` para que un modelo de Inteligencia Artificial (ej. Aprendizaje por Refuerzo) ajuste dinámicamente los intervalos de mensajes de control del protocolo según la velocidad detectada en la red.