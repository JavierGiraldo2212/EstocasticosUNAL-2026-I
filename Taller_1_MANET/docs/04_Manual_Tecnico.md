# 04. Manual Técnico: Simulación de MANET Jerárquica

## 1. Arquitectura de Software (NS-3)
El script de simulación (`manet_jerarquica.cc`) está desarrollado en C++ utilizando las librerías estándar del núcleo de NS-3. El sistema se diseñó de forma modular para instanciar una topología de red de dos niveles.

## 2. Clases y Helpers Principales Utilizados
* **Contenedores de Nodos (`NodeContainer`):** Se instanciaron cinco contenedores independientes para representar lógicamente la jerarquía (3 clústeres hoja y 2 clústeres troncales o *backbone*).
* **Capa Física y Enlace (`YansWifiPhyHelper`, `WifiMacHelper`):** Se configuró la red bajo el estándar IEEE 802.11g en modo *Ad Hoc* (`ns3::AdhocWifiMac`), garantizando que no exista una infraestructura central.
* **Gestión de Movilidad (`MobilityHelper`):** * *Nivel 1 (Nodos Hoja):* Se implementó el modelo `RandomWalk2dMobilityModel` para simular el desplazamiento local y pseudoaleatorio de los dispositivos individuales.
    * *Nivel 2 (Backbone):* Se implementó el modelo `GaussMarkovMobilityModel` para simular el movimiento direccional coordinado del clúster troncal.
* **Enrutamiento (`AodvHelper`):** Se integró el protocolo reactivo AODV en la pila de red (`InternetStackHelper`) para gestionar dinámicamente las rutas multi-salto y reaccionar a las rupturas de enlaces causadas por la movilidad.

## 3. Extracción de Métricas
El sistema utiliza la clase `FlowMonitorHelper` para inspeccionar el tráfico a nivel de red (IPv4). Al finalizar la simulación, el objeto `FlowMonitor` serializa los resultados y genera un archivo `manet-metrics.xml`, el cual contiene estadísticas precisas sobre *Throughput*, pérdida de paquetes y latencia.