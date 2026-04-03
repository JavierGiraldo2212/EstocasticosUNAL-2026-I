/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/**
 * Taller 1: Modelos Estocásticos y Simulación
 * Tema: MANET Jerárquica con Movilidad Dual
 * Estructura: 3 Clústeres Nivel 1 (Hojas), 2 Clústeres Nivel 2 (Backbone)
 */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/aodv-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("ManetJerarquicaTaller1");

int main (int argc, char *argv[])
{
  // ------------------------------------------------------------
  // 1. CONFIGURACIÓN DE PARÁMETROS (Para los 3 escenarios)
  // ------------------------------------------------------------
  double velocityL2 = 2.0; // Velocidad de los clústeres Nivel 2 (por defecto Escenario 1)
  uint32_t simTime = 100;  // Tiempo de simulación en segundos
  
  CommandLine cmd;
  cmd.AddValue ("velocityL2", "Velocidad global de clústeres Nivel 2 (m/s)", velocityL2);
  cmd.AddValue ("simTime", "Tiempo total de simulación", simTime);
  cmd.Parse (argc, argv);

  NS_LOG_INFO ("Iniciando Simulación MANET Jerárquica a velocidad L2 = " << velocityL2 << " m/s");

  // ------------------------------------------------------------
  // 2. CREACIÓN DE NODOS (Jerarquía)
  // ------------------------------------------------------------
  // Nivel 1: Leaf Clusters (3 clústeres de 5 nodos cada uno)
  NodeContainer clusterL1_A, clusterL1_B, clusterL1_C;
  clusterL1_A.Create (5);
  clusterL1_B.Create (5);
  clusterL1_C.Create (5);

  // Nivel 2: Backbone Clusters (2 clústeres de 3 nodos cada uno)
  NodeContainer clusterL2_X, clusterL2_Y;
  clusterL2_X.Create (3);
  clusterL2_Y.Create (3);

  // Contenedor general para facilitar la instalación de dispositivos
  NodeContainer allNodes;
  allNodes.Add (clusterL1_A);
  allNodes.Add (clusterL1_B);
  allNodes.Add (clusterL1_C);
  allNodes.Add (clusterL2_X);
  allNodes.Add (clusterL2_Y);

  // ------------------------------------------------------------
  // 3. CAPA FÍSICA Y MAC (Wi-Fi Ad Hoc)
  // ------------------------------------------------------------
  WifiHelper wifi;
  wifi.SetStandard (WIFI_STANDARD_80211g);

  YansWifiPhyHelper wifiPhy;
  YansWifiChannelHelper wifiChannel = YansWifiChannelHelper::Default ();
  wifiPhy.SetChannel (wifiChannel.Create ());

  WifiMacHelper wifiMac;
  wifiMac.SetType ("ns3::AdhocWifiMac"); // Modo Ad Hoc

  NetDeviceContainer allDevices = wifi.Install (wifiPhy, wifiMac, allNodes);

  // ------------------------------------------------------------
  // 4. MOVILIDAD (Movilidad de Nodo y Clúster ajustada a 250x250m)
  // ------------------------------------------------------------
  MobilityHelper mobility;

  // Asignamos una posición inicial aleatoria en un área concentrada (250x250)
  mobility.SetPositionAllocator ("ns3::RandomRectanglePositionAllocator",
                                 "X", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=250.0]"),
                                 "Y", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=250.0]"));

  // Movilidad de los Nodos del Nivel 1 (Movimiento local aleatorio dentro del área)
  mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
                             "Bounds", RectangleValue (Rectangle (0.0, 250.0, 0.0, 250.0)),
                             "Speed", StringValue ("ns3::ConstantRandomVariable[Constant=1.0]"));
  mobility.Install (clusterL1_A);
  mobility.Install (clusterL1_B);
  mobility.Install (clusterL1_C);

  // Movilidad de los Clústeres del Nivel 2 (Movimiento en bloque, dictado por el parámetro velocityL2)
  std::ostringstream speedString;
  speedString << "ns3::ConstantRandomVariable[Constant=" << velocityL2 << "]";
  
  mobility.SetMobilityModel ("ns3::GaussMarkovMobilityModel",
                             "Bounds", BoxValue (Box (0.0, 250.0, 0.0, 250.0, 0.0, 10.0)),
                             "TimeStep", TimeValue (Seconds (0.5)),
                             "Alpha", DoubleValue (0.85),
                             "MeanVelocity", StringValue (speedString.str ()));
  mobility.Install (clusterL2_X);
  mobility.Install (clusterL2_Y);

  // ------------------------------------------------------------
  // 5. ENRUTAMIENTO (AODV) Y PILA DE RED
  // ------------------------------------------------------------
  AodvHelper aodv;
  InternetStackHelper internet;
  internet.SetRoutingHelper (aodv); // Usamos AODV para lidiar con rupturas de enlaces
  internet.Install (allNodes);

  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer allInterfaces = ipv4.Assign (allDevices);

  // ------------------------------------------------------------
  // 6. TRÁFICO Y APLICACIONES (Generando datos para evaluar)
  // ------------------------------------------------------------
  // Enviamos tráfico desde el Nodo 0 (Clúster L1_A) hacia el último Nodo (Clúster L1_C)
  uint16_t port = 9;
  UdpEchoServerHelper server (port);
  ApplicationContainer serverApps = server.Install (clusterL1_C.Get (4)); // Nodo destino
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (simTime - 1.0));

  UdpEchoClientHelper client (allInterfaces.GetAddress (allNodes.GetN () - 1), port);
  client.SetAttribute ("MaxPackets", UintegerValue (1000));
  client.SetAttribute ("Interval", TimeValue (Seconds (0.1))); // 10 paquetes por segundo
  client.SetAttribute ("PacketSize", UintegerValue (1024));

  ApplicationContainer clientApps = client.Install (clusterL1_A.Get (0)); // Nodo origen
  clientApps.Start (Seconds (2.0));
  clientApps.Stop (Seconds (simTime - 2.0));

  // ------------------------------------------------------------
  // 7. MONITOREO Y EXTRACCIÓN DE MÉTRICAS
  // ------------------------------------------------------------
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  // ------------------------------------------------------------
  // 8. EJECUCIÓN DE LA SIMULACIÓN
  // ------------------------------------------------------------
  Simulator::Stop (Seconds (simTime));
  Simulator::Run ();

  // Exportar resultados de FlowMonitor a un archivo XML
  monitor->SerializeToXmlFile ("manet-metrics.xml", true, true);

  Simulator::Destroy ();
  NS_LOG_INFO ("Simulación finalizada.");

  return 0;
}