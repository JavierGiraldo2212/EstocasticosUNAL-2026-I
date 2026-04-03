# 02. Descripcion Justificacion

## 1. Descripción del Problema e Indagación Científica
El presente proyecto aborda el desafío del enrutamiento y la estabilidad en Redes Móviles Ad Hoc (MANET) bajo condiciones de movilidad grupal. Siguiendo las directrices del taller, se plantea un sistema MANET jerárquico estructurado en dos niveles: un primer nivel compuesto por tres (3) clústeres de nodos hoja, y un segundo nivel compuesto por dos (2) clústeres troncales o *backbone*.

Bajo este contexto, y aplicando el método científico, se formula la siguiente **indagación principal**:
> *¿De qué manera la velocidad de desplazamiento global de los clústeres de segundo nivel afecta la estabilidad de las rutas y el throughput (rendimiento) de las comunicaciones entre los nodos del primer nivel?*

## 2. Justificación
En escenarios de aplicación real, como operaciones de rescate, despliegues tácticos militares o enjambres de vehículos autónomos (drones/vehículos), los nodos no se mueven de forma caótica y aislada. Por el contrario, exhiben una movilidad coordinada (movimiento a nivel de clúster) sumada a desplazamientos locales (movimiento a nivel de nodo). 

Simular este comportamiento jerárquico en NS-3 es fundamental para evaluar si los protocolos de enrutamiento tradicionales soportan la ruptura frecuente de enlaces inter-clúster generada por altas velocidades, o si la red sufre una degradación inaceptable.

## 3. Hipótesis
Se postula que, al incrementar la velocidad de desplazamiento de los clústeres de segundo nivel (encargados de enrutar el tráfico inter-clúster), se producirá un aumento exponencial en la tasa de ruptura de enlaces. Esto obligará a los nodos a recalcular rutas constantemente, lo que incrementará el *overhead* de control en la red y disminuirá significativamente el *throughput* y el *Packet Delivery Ratio* (PDR) de los nodos de primer nivel.

## 4. Diseño Experimental (Metodología)
Para comprobar la hipótesis y dar respuesta a la indagación, el sistema permitirá el movimiento tanto a nivel de nodo como de clúster. La evaluación se realizará mediante la ejecución y documentación de tres (3) escenarios de prueba obligatorios:
* **Escenario 1 (Control - Baja Movilidad):** Clústeres de segundo nivel desplazándose a velocidades peatonales (ej. 1 - 2 m/s). Servirá como línea base.
* **Escenario 2 (Movilidad Moderada):** Clústeres de segundo nivel con velocidades vehiculares urbanas (ej. 15 m/s).
* **Escenario 3 (Estrés - Alta Movilidad):** Clústeres de segundo nivel a altas velocidades (ej. 30 m/s) para encontrar el punto de quiebre de la topología jerárquica.