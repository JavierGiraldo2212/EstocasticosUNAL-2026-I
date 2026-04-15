/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/**
 * Taller 1: Modelos Estocásticos y Simulación
 * Tema: MANET Jerárquica con Movilidad Dual
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
  // ── 1. PARÁMETROS ──────────────────────────────────────────
  double velocityL2   = 2.0;
  uint32_t simTime    = 100;
  std::string outFile = "metrics_escenario_1.xml";

  CommandLine cmd;
  cmd.AddValue ("velocityL2", "Velocidad backbone L2 (m/s)", velocityL2);
  cmd.AddValue ("simTime",    "Tiempo de simulación (s)",    simTime);
  cmd.AddValue ("outFile",    "Archivo XML de salida",       outFile);
  cmd.Parse (argc, argv);

  NS_LOG_INFO ("Velocidad L2 = " << velocityL2 << " m/s | Salida: " << outFile);

  // ── 2. NODOS ───────────────────────────────────────────────
  // Nivel 1: 3 clústeres × 5 nodos = 15 nodos (índices 0-14)
  NodeContainer clusterL1_A, clusterL1_B, clusterL1_C;
  clusterL1_A.Create (5);   // índices 0-4
  clusterL1_B.Create (5);   // índices 5-9
  clusterL1_C.Create (5);   // índices 10-14

  // Nivel 2: 2 clústeres × 3 nodos = 6 nodos (índices 15-20)
  NodeContainer clusterL2_X, clusterL2_Y;
  clusterL2_X.Create (3);   // índices 15-17
  clusterL2_Y.Create (3);   // índices 18-20

  NodeContainer allNodes;
  allNodes.Add (clusterL1_A);
  allNodes.Add (clusterL1_B);
  allNodes.Add (clusterL1_C);
  allNodes.Add (clusterL2_X);
  allNodes.Add (clusterL2_Y);

  // ── 3. WIFI AD HOC ─────────────────────────────────────────
  WifiHelper wifi;
  wifi.SetStandard (WIFI_STANDARD_80211g);
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
                                 "DataMode",    StringValue ("ErpOfdmRate6Mbps"),
                                 "ControlMode", StringValue ("ErpOfdmRate6Mbps"));

  YansWifiPhyHelper wifiPhy;
  YansWifiChannelHelper wifiChannel = YansWifiChannelHelper::Default ();
  wifiPhy.SetChannel (wifiChannel.Create ());

  WifiMacHelper wifiMac;
  wifiMac.SetType ("ns3::AdhocWifiMac");

  NetDeviceContainer allDevices = wifi.Install (wifiPhy, wifiMac, allNodes);

  // ── 4. MOVILIDAD ───────────────────────────────────────────
  MobilityHelper mobility;

  // Posición inicial aleatoria en 250×250 m
  mobility.SetPositionAllocator (
      "ns3::RandomRectanglePositionAllocator",
      "X", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=250.0]"),
      "Y", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=250.0]"));

  // Nivel 1: RandomWalk2D — movimiento local de nodos
  mobility.SetMobilityModel (
      "ns3::RandomWalk2dMobilityModel",
      "Bounds", RectangleValue (Rectangle (0.0, 250.0, 0.0, 250.0)),
      "Speed",  StringValue ("ns3::ConstantRandomVariable[Constant=1.0]"),
      "Distance", DoubleValue (30.0));   // cambia dirección cada 30 m
  mobility.Install (clusterL1_A);
  mobility.Install (clusterL1_B);
  mobility.Install (clusterL1_C);

  // Nivel 2: Gauss-Markov — movimiento de clúster backbone
  std::ostringstream speedStr;
  speedStr << "ns3::ConstantRandomVariable[Constant=" << velocityL2 << "]";

  mobility.SetMobilityModel (
      "ns3::GaussMarkovMobilityModel",
      "Bounds",        BoxValue (Box (0.0, 250.0, 0.0, 250.0, 0.0, 10.0)),
      "TimeStep",      TimeValue (Seconds (0.5)),
      "Alpha",         DoubleValue (0.85),
      "MeanVelocity",  StringValue (speedStr.str ()),
      "MeanDirection", StringValue ("ns3::UniformRandomVariable[Min=0|Max=6.283185]"),
      "MeanPitch",     StringValue ("ns3::ConstantRandomVariable[Constant=0.0]"));
  mobility.Install (clusterL2_X);
  mobility.Install (clusterL2_Y);

  // ── 5. PILA DE RED + AODV ──────────────────────────────────
  AodvHelper aodv;
  InternetStackHelper internet;
  internet.SetRoutingHelper (aodv);
  internet.Install (allNodes);

  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer allIfaces = ipv4.Assign (allDevices);

  // ── 6. APLICACIONES ────────────────────────────────────────
  uint16_t port = 9;

  // Servidor en clusterL1_C nodo 4 → índice global 14
  UdpEchoServerHelper server (port);
  ApplicationContainer serverApps = server.Install (clusterL1_C.Get (4));
  serverApps.Start (Seconds (1.0));
  serverApps.Stop  (Seconds (simTime - 1.0));

  // Cliente en clusterL1_A nodo 0 → índice global 0
  // Dirección destino = IP del nodo 14
  UdpEchoClientHelper client (allIfaces.GetAddress (14), port);
  client.SetAttribute ("MaxPackets", UintegerValue (1000));
  client.SetAttribute ("Interval",   TimeValue (Seconds (0.1)));
  client.SetAttribute ("PacketSize", UintegerValue (1024));

  ApplicationContainer clientApps = client.Install (clusterL1_A.Get (0));
  clientApps.Start (Seconds (2.0));
  clientApps.Stop  (Seconds (simTime - 2.0));

  // ── 7. FLOW MONITOR ────────────────────────────────────────
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  // ── 8. SIMULACIÓN ──────────────────────────────────────────
  Simulator::Stop (Seconds (simTime));
  Simulator::Run ();

  monitor->CheckForLostPackets ();
  monitor->SerializeToXmlFile (outFile, true, true);

  Simulator::Destroy ();
  NS_LOG_INFO ("Simulación finalizada. XML: " << outFile);
  return 0;
}
