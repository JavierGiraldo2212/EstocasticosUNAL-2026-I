# 04. Manual Técnico: Simulación de MANET Jerárquica

## 1. Arquitectura de Software (NS-3)
El script de simulación (`manet_jerarquica.cc`) está desarrollado en C++ utilizando las librerías estándar del núcleo de NS-3. El sistema se diseñó de forma modular para instanciar una topología de red de dos niveles. Además, la arquitectura integra la clase `CommandLine` para exponer parámetros globales (como la velocidad del clúster y el protocolo a evaluar), permitiendo la automatización de la experimentación desde la terminal sin necesidad de recompilar el código fuente.

## 2. Clases y Helpers Principales Utilizados
* **Contenedores de Nodos (`NodeContainer`):** Se instanciaron cinco contenedores independientes para representar lógicamente la jerarquía (3 clústeres hoja y 2 clústeres troncales o *backbone*).
* **Capa Física y Enlace (`YansWifiPhyHelper`, `WifiMacHelper`):** Se configuró la red bajo el estándar IEEE 802.11g en modo *Ad Hoc* (`ns3::AdhocWifiMac`), garantizando que no exista una infraestructura central.
* **Gestión de Movilidad (`MobilityHelper`):** * *Nivel 1 (Nodos Hoja):* Se implementó el modelo `RandomWalk2dMobilityModel` para simular el desplazamiento local y pseudoaleatorio de los dispositivos individuales.
    * *Nivel 2 (Backbone):* Se implementó el modelo `GaussMarkovMobilityModel` para simular el movimiento direccional coordinado del clúster troncal.
* **Enrutamiento Dinámico (`AodvHelper` y `OlsrHelper`):** Se implementó una lógica condicional en la pila de red (`InternetStackHelper`). Dependiendo del parámetro ingresado, el sistema inyecta el protocolo reactivo AODV o el protocolo proactivo OLSR para gestionar las rutas multi-salto. Esto permite evaluar de forma cruzada cómo reacciona cada paradigma a las rupturas de enlaces causadas por la movilidad.

## 3. Extracción de Métricas
El sistema utiliza la clase `FlowMonitorHelper` para inspeccionar el tráfico a nivel de red (IPv4). Al finalizar la simulación, el objeto `FlowMonitor` serializa los resultados y genera un archivo XML de forma dinámica concatenando el nombre del protocolo evaluado (ej. `metrics_AODV.xml` o `metrics_OLSR.xml`) para evitar la sobrescritura de datos. Este archivo contiene estadísticas precisas sobre *Throughput*, pérdida de paquetes y latencia.