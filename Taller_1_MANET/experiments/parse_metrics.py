import xml.etree.ElementTree as ET
import os
import glob

def analyze_xml(xml_file, label):
    if not os.path.exists(xml_file):
        print(f"[AVISO] No encontrado: {xml_file}")
        return

    tree = ET.parse(xml_file)
    root = tree.getroot()

    total_tx   = 0
    total_rx   = 0
    total_bytes = 0
    total_delay = 0.0
    n_flows     = 0

    for flow in root.findall('.//FlowStats/Flow'):
        tx = int(flow.get('txPackets', 0))
        rx = int(flow.get('rxPackets', 0))
        rb = int(flow.get('rxBytes',   0))

        # La latencia viene en nanosegundos como "Xns"
        delay_str = flow.get('delaySum', '0ns').replace('ns','')
        try:
            delay_ns = float(delay_str)
        except ValueError:
            delay_ns = 0.0

        total_tx    += tx
        total_rx    += rx
        total_bytes += rb
        if rx > 0:
            total_delay += delay_ns / rx
        n_flows += 1

    pdr        = (total_rx / total_tx * 100) if total_tx > 0 else 0
    throughput = (total_bytes * 8) / (100 * 1000)  # Kbps en 100s
    avg_delay  = (total_delay / n_flows / 1e6) if n_flows > 0 else 0  # ms

    print(f"{'='*45}")
    print(f"  {label}")
    print(f"{'='*45}")
    print(f"  Flujos detectados     : {n_flows}")
    print(f"  Paquetes TX           : {total_tx}")
    print(f"  Paquetes RX           : {total_rx}")
    print(f"  PDR                   : {pdr:.2f} %")
    print(f"  Throughput            : {throughput:.2f} Kbps")
    print(f"  Latencia media        : {avg_delay:.3f} ms")
    print()

if __name__ == "__main__":
    base = "/home/javier-giraldo/ns-allinone-3.43/ns-3.43/"

    scenarios = [
        # Resultados para AODV
        (f"{base}metrics_AODV_2.xml",  "AODV - Escenario 1 (Control: 2 m/s)"),
        (f"{base}metrics_AODV_15.xml", "AODV - Escenario 2 (Moderado: 15 m/s)"),
        (f"{base}metrics_AODV_30.xml", "AODV - Escenario 3 (Estrés: 30 m/s)"),
        
        # Resultados para OLSR
        (f"{base}metrics_OLSR_2.xml",  "OLSR - Escenario 1 (Control: 2 m/s)"),
        (f"{base}metrics_OLSR_15.xml", "OLSR - Escenario 2 (Moderado: 15 m/s)"),
        (f"{base}metrics_OLSR_30.xml", "OLSR - Escenario 3 (Estrés: 30 m/s)"),
    ]

    print("\nIniciando análisis comparativo: AODV vs OLSR...\n")
    for xml_path, label in scenarios:
        analyze_xml(xml_path, label)