# 02. Descripción, Justificación e Hipótesis

## 1. Descripción del Problema e Indagación Científica
El presente proyecto aborda el desafío del enrutamiento y la estabilidad en Redes Móviles Ad Hoc (MANET) bajo condiciones de movilidad grupal. Siguiendo las directrices del taller, se plantea un sistema MANET jerárquico estructurado en dos niveles: un primer nivel compuesto por tres (3) clústeres de nodos hoja, y un segundo nivel compuesto por dos (2) clústeres troncales o *backbone*.

Bajo este contexto, y aplicando el método científico, se amplía el alcance de la simulación para contrastar paradigmas de enrutamiento, formulando la siguiente **indagación principal**:
> *¿De qué manera la velocidad de desplazamiento global de los clústeres de segundo nivel afecta la estabilidad de las rutas, la latencia y el throughput (rendimiento) de las comunicaciones entre los nodos del primer nivel al comparar un protocolo de enrutamiento reactivo (AODV) frente a uno proactivo (OLSR)?*

## 2. Justificación
En escenarios de aplicación real, como operaciones de rescate, despliegues tácticos militares o enjambres de vehículos autónomos (drones/vehículos), los nodos no se mueven de forma caótica y aislada. Por el contrario, exhiben una movilidad coordinada (movimiento a nivel de clúster) sumada a desplazamientos locales (movimiento a nivel de nodo). 

Simular este comportamiento jerárquico en NS-3 es fundamental para evaluar si los protocolos de enrutamiento tradicionales soportan la ruptura frecuente de enlaces inter-clúster generada por altas velocidades, o si la red sufre una degradación inaceptable. Además, determinar el protocolo adecuado es crítico: un protocolo reactivo (AODV) podría colapsar por la saturación de peticiones de ruta al romperse los enlaces, mientras que uno proactivo (OLSR) podría fallar al no poder mantener sus tablas sincronizadas con los rápidos cambios topológicos.

## 3. Hipótesis
Se postula que, al incrementar la velocidad de desplazamiento de los clústeres de segundo nivel (encargados de enrutar el tráfico inter-clúster), se producirá un aumento exponencial en la tasa de ruptura de enlaces. 

Frente a este fenómeno, se hipotetiza que en escenarios de baja y moderada movilidad, el protocolo proactivo (OLSR) superará ampliamente al reactivo (AODV), ofreciendo latencias mínimas al tener las rutas precalculadas. Sin embargo, al alcanzar velocidades de estrés (ej. 30 m/s), la velocidad de ruptura de enlaces superará la frecuencia de actualización de los mensajes de control de topología de OLSR (generando rutas caducadas). Esto obligará a ambos protocolos a fallar, incrementando el *overhead* de control en la red y disminuyendo significativamente el *throughput* y el *Packet Delivery Ratio* (PDR) de los nodos de primer nivel.

## 4. Diseño Experimental (Metodología)
Para comprobar la hipótesis y dar respuesta a la indagación, el sistema permitirá el movimiento tanto a nivel de nodo como de clúster. La evaluación se realizará mediante la ejecución cruzada de los dos protocolos sobre tres (3) escenarios de velocidad obligatorios, resultando en un total de seis (6) pruebas documentadas:
* **Escenarios 1 (Control - Baja Movilidad):** Clústeres de segundo nivel desplazándose a velocidades peatonales (ej. 2 m/s). Servirá como línea base para evaluar el establecimiento inicial de rutas en AODV y OLSR.
* **Escenarios 2 (Movilidad Moderada):** Clústeres de segundo nivel con velocidades vehiculares urbanas (ej. 15 m/s).
* **Escenarios 3 (Estrés - Alta Movilidad):** Clústeres de segundo nivel a altas velocidades (ej. 30 m/s) para encontrar el punto de quiebre de la topología jerárquica bajo ambos paradigmas de enrutamiento.