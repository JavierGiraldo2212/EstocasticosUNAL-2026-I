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
#include "ns3/olsr-module.h" // <-- NUEVA LIBRERÍA: OLSR
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("ManetJerarquicaTaller1");

int main (int argc, char *argv[])
{
  // ------------------------------------------------------------
  // 1. CONFIGURACIÓN DE PARÁMETROS (Para los 3 escenarios + Protocolos)
  // ------------------------------------------------------------
  double velocityL2 = 2.0; 
  uint32_t simTime = 100;  
  std::string protocol = "AODV"; // <-- NUEVO PARÁMETRO: Protocolo por defecto
  
  CommandLine cmd;
  cmd.AddValue ("velocityL2", "Velocidad global de clústeres Nivel 2 (m/s)", velocityL2);
  cmd.AddValue ("protocol", "Protocolo de enrutamiento a evaluar (AODV u OLSR)", protocol);
  cmd.AddValue ("simTime", "Tiempo total de simulación", simTime);
  cmd.Parse (argc, argv);

  NS_LOG_INFO ("Iniciando MANET | Velocidad L2: " << velocityL2 << " m/s | Protocolo: " << protocol);

  // ------------------------------------------------------------
  // 2. CREACIÓN DE NODOS (Jerarquía)
  // ------------------------------------------------------------
  NodeContainer clusterL1_A, clusterL1_B, clusterL1_C;
  clusterL1_A.Create (5);
  clusterL1_B.Create (5);
  clusterL1_C.Create (5);

  NodeContainer clusterL2_X, clusterL2_Y;
  clusterL2_X.Create (3);
  clusterL2_Y.Create (3);

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
  wifiMac.SetType ("ns3::AdhocWifiMac"); 
  NetDeviceContainer allDevices = wifi.Install (wifiPhy, wifiMac, allNodes);

  // ------------------------------------------------------------
  // 4. MOVILIDAD (Área concentrada 250x250m)
  // ------------------------------------------------------------
  MobilityHelper mobility;
  mobility.SetPositionAllocator ("ns3::RandomRectanglePositionAllocator",
                                 "X", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=250.0]"),
                                 "Y", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=250.0]"));

  mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
                             "Bounds", RectangleValue (Rectangle (0.0, 250.0, 0.0, 250.0)),
                             "Speed", StringValue ("ns3::ConstantRandomVariable[Constant=1.0]"));
  mobility.Install (clusterL1_A);
  mobility.Install (clusterL1_B);
  mobility.Install (clusterL1_C);

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
  // 5. ENRUTAMIENTO DINÁMICO (AODV vs OLSR) Y PILA DE RED
  // ------------------------------------------------------------
  InternetStackHelper internet;
  
  // Selección condicional basada en el parámetro ingresado
  if (protocol == "AODV") {
      AodvHelper aodv;
      internet.SetRoutingHelper (aodv);
  } else if (protocol == "OLSR") {
      OlsrHelper olsr;
      internet.SetRoutingHelper (olsr);
  } else {
      NS_FATAL_ERROR ("Protocolo no soportado. Use AODV o OLSR.");
  }
  
  internet.Install (allNodes);

  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer allInterfaces = ipv4.Assign (allDevices);

  // ------------------------------------------------------------
  // 6. TRÁFICO Y APLICACIONES
  // ------------------------------------------------------------
  uint16_t port = 9;
  UdpEchoServerHelper server (port);
  ApplicationContainer serverApps = server.Install (clusterL1_C.Get (4)); 
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (simTime - 1.0));

  UdpEchoClientHelper client (allInterfaces.GetAddress (allNodes.GetN () - 1), port);
  client.SetAttribute ("MaxPackets", UintegerValue (1000));
  client.SetAttribute ("Interval", TimeValue (Seconds (0.1))); 
  client.SetAttribute ("PacketSize", UintegerValue (1024));

  ApplicationContainer clientApps = client.Install (clusterL1_A.Get (0)); 
  clientApps.Start (Seconds (2.0));
  clientApps.Stop (Seconds (simTime - 2.0));

  // ------------------------------------------------------------
  // 7. MONITOREO Y EJECUCIÓN
  // ------------------------------------------------------------
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  Simulator::Stop (Seconds (simTime));
  Simulator::Run ();

  // Exportamos con un nombre dinámico para no sobreescribir AODV con OLSR
  std::string xmlFileName = "metrics_" + protocol + ".xml";
  monitor->SerializeToXmlFile (xmlFileName, true, true);

  Simulator::Destroy ();
  NS_LOG_INFO ("Simulación finalizada.");

  return 0;
}