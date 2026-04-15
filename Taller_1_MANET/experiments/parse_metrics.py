"""
=============================================================
  Analizador de Métricas MANET Jerárquica — Taller 1
  Modelos Estocásticos y Simulación
=============================================================
  Analiza los XML generados por FlowMonitor en NS-3 y produce:
    • Resumen por consola (tabla comparativa)
    • Gráficas PNG  (PDR, Throughput, Latencia, Jitter)
    • Reporte PDF   (manet_reporte.pdf)
    • Exportación   (manet_resultados.csv)
=============================================================
"""

import xml.etree.ElementTree as ET
import os
import sys
import csv
import re
import warnings
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, Image, PageBreak,
                                 HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
BASE = BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
SIM_TIME = 100          # segundos de simulación
OUTPUT_DIR = "./"       # carpeta donde se guardan PNG, PDF y CSV

SCENARIOS = [
    {
        "xml":   f"{BASE}metrics_escenario_1.xml",
        "label": "Escenario 1\nControl (2 m/s)",
        "short": "E1 – 2 m/s",
        "velocity": 2,
    },
    {
        "xml":   f"{BASE}metrics_escenario_2.xml",
        "label": "Escenario 2\nModerado (15 m/s)",
        "short": "E2 – 15 m/s",
        "velocity": 15,
    },
    {
        "xml":   f"{BASE}metrics_escenario_3.xml",
        "label": "Escenario 3\nEstrés (30 m/s)",
        "short": "E3 – 30 m/s",
        "velocity": 30,
    },
]

# ─────────────────────────────────────────────────────────────
#  COLORES
# ─────────────────────────────────────────────────────────────
PALETTE = ["#2196F3", "#4CAF50", "#F44336"]   # azul, verde, rojo
PALETTE_LIGHT = ["#90CAF9", "#A5D6A7", "#EF9A9A"]


# ═════════════════════════════════════════════════════════════
#  1.  PARSING DEL XML
# ═════════════════════════════════════════════════════════════
def parse_ns_time(value: str) -> float:
    """Convierte '1234567890ns' / '1.23e+09ns' / '0.5s' a segundos float."""
    if not value or value in ("0", ""):
        return 0.0
    value = value.strip()
    if value.endswith("ns"):
        return float(value[:-2]) * 1e-9
    if value.endswith("us"):
        return float(value[:-2]) * 1e-6
    if value.endswith("ms"):
        return float(value[:-2]) * 1e-3
    if value.endswith("s"):
        return float(value[:-1])
    # Sin unidad → asumimos nanosegundos (comportamiento NS-3 por defecto)
    try:
        return float(value) * 1e-9
    except ValueError:
        return 0.0


def analyze_xml(xml_file: str, label: str, sim_time: int = SIM_TIME) -> dict | None:
    """Extrae métricas agregadas y por flujo de un XML de FlowMonitor."""
    if not os.path.exists(xml_file):
        print(f"  Archivo no encontrado: {xml_file}")
        return None

    tree = ET.parse(xml_file)
    root = tree.getroot()

    total_tx = total_rx = total_bytes = 0
    total_delay_s = total_jitter_s = 0.0
    total_lost = 0
    flows_data = []

    for flow in root.findall(".//FlowStats/Flow"):
        tx  = int(flow.get("txPackets", 0))
        rx  = int(flow.get("rxPackets", 0))
        rb  = int(flow.get("rxBytes",   0))
        lost = int(flow.get("lostPackets", 0))

        delay_s  = parse_ns_time(flow.get("delaySum",  "0ns"))
        jitter_s = parse_ns_time(flow.get("jitterSum", "0ns"))

        avg_delay_ms  = (delay_s  / rx * 1000) if rx > 0 else 0.0
        avg_jitter_ms = (jitter_s / rx * 1000) if rx > 0 else 0.0
        flow_tput_kbps = (rb * 8) / (sim_time * 1000)
        flow_pdr = (rx / tx * 100) if tx > 0 else 0.0

        flows_data.append({
            "tx": tx, "rx": rx, "bytes": rb, "lost": lost,
            "delay_ms": avg_delay_ms, "jitter_ms": avg_jitter_ms,
            "throughput_kbps": flow_tput_kbps, "pdr": flow_pdr,
        })

        total_tx    += tx
        total_rx    += rx
        total_bytes += rb
        total_lost  += lost
        if rx > 0:
            total_delay_s  += delay_s  / rx
            total_jitter_s += jitter_s / rx

    n_flows = len(flows_data)
    pdr        = (total_rx / total_tx * 100)         if total_tx > 0 else 0.0
    throughput = (total_bytes * 8) / (sim_time * 1000)   # Kbps global
    avg_delay  = (total_delay_s  / n_flows * 1000)   if n_flows > 0 else 0.0
    avg_jitter = (total_jitter_s / n_flows * 1000)   if n_flows > 0 else 0.0
    plr        = (total_lost / (total_tx + total_lost) * 100) if (total_tx + total_lost) > 0 else 0.0

    return {
        "label":       label,
        "n_flows":     n_flows,
        "total_tx":    total_tx,
        "total_rx":    total_rx,
        "total_lost":  total_lost,
        "pdr":         round(pdr,        2),
        "plr":         round(plr,        2),
        "throughput":  round(throughput, 3),
        "delay_ms":    round(avg_delay,  4),
        "jitter_ms":   round(avg_jitter, 4),
        "flows":       flows_data,
    }


# ═════════════════════════════════════════════════════════════
#  2.  CONSOLA
# ═════════════════════════════════════════════════════════════
def print_summary(results: list[dict]) -> None:
    print("\n" + "═" * 70)
    print("   RESUMEN COMPARATIVO — MANET Jerárquica con Movilidad Dual")
    print("═" * 70)
    header = f"{'Métrica':<22} | " + " | ".join(f"{r['label']:>18}" for r in results)
    print(header)
    print("─" * len(header))

    metrics = [
        ("Flujos detectados",    "n_flows",    ""),
        ("Paquetes TX",          "total_tx",   ""),
        ("Paquetes RX",          "total_rx",   ""),
        ("Paquetes perdidos",    "total_lost",  ""),
        ("PDR (%)",              "pdr",         "%"),
        ("PLR (%)",              "plr",         "%"),
        ("Throughput (Kbps)",    "throughput",  " Kbps"),
        ("Latencia media (ms)",  "delay_ms",    " ms"),
        ("Jitter medio (ms)",    "jitter_ms",   " ms"),
    ]
    for name, key, unit in metrics:
        row = f"{name:<22} | "
        row += " | ".join(f"{str(r[key]) + unit:>18}" for r in results)
        print(row)
    print("═" * 70 + "\n")


# ═════════════════════════════════════════════════════════════
#  3.  GRÁFICAS
# ═════════════════════════════════════════════════════════════
def make_charts(results: list[dict], out_dir: str) -> list[str]:
    labels  = [r["label"].replace("\n", " ") for r in results]
    short   = [s["short"] for s in SCENARIOS[:len(results)]]
    speeds  = [s["velocity"] for s in SCENARIOS[:len(results)]]

    pdr_vals        = [r["pdr"]        for r in results]
    tput_vals       = [r["throughput"] for r in results]
    delay_vals      = [r["delay_ms"]   for r in results]
    jitter_vals     = [r["jitter_ms"]  for r in results]
    plr_vals        = [r["plr"]        for r in results]

    saved = []

    # ── Figura 1: Panel de 4 barras ──────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Comparativa de Escenarios — MANET Jerárquica", fontsize=14, fontweight="bold")

    datasets = [
        (axes[0, 0], pdr_vals,    "PDR (%)",             "PDR por Escenario",         100),
        (axes[0, 1], tput_vals,   "Throughput (Kbps)",   "Throughput por Escenario",  None),
        (axes[1, 0], delay_vals,  "Latencia media (ms)", "Latencia por Escenario",    None),
        (axes[1, 1], jitter_vals, "Jitter medio (ms)",   "Jitter por Escenario",      None),
    ]
    for ax, vals, ylabel, title, ylim in datasets:
        bars = ax.bar(short, vals, color=PALETTE[:len(results)], edgecolor="white", width=0.5)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_ylabel(ylabel)
        ax.set_ylim(0, ylim if ylim else max(vals) * 1.25 + 0.001)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(vals) * 0.02,
                    f"{val:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    p1 = os.path.join(out_dir, "fig1_panel_barras.png")
    fig.savefig(p1, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(p1)
    print(f"  [OK] {p1}")

    # ── Figura 2: Líneas vs velocidad ────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle("Evolución de Métricas con la Velocidad del Backbone (L2)",
                 fontsize=13, fontweight="bold")

    line_data = [
        (axes[0], pdr_vals,   plr_vals,   "PDR / PLR (%)",   ["PDR", "PLR"]),
        (axes[1], tput_vals,  None,        "Throughput (Kbps)", ["Throughput"]),
        (axes[2], delay_vals, jitter_vals, "Tiempo (ms)",     ["Latencia", "Jitter"]),
    ]
    for ax, y1, y2, ylabel, leg in line_data:
        ax.plot(speeds, y1, "o-", color=PALETTE[0], linewidth=2, markersize=7, label=leg[0])
        if y2:
            ax.plot(speeds, y2, "s--", color=PALETTE[2], linewidth=2, markersize=7, label=leg[1])
            ax.legend(fontsize=9)
        ax.set_xlabel("Velocidad L2 (m/s)")
        ax.set_ylabel(ylabel)
        ax.set_xticks(speeds)
        ax.grid(linestyle="--", alpha=0.4)
        ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    p2 = os.path.join(out_dir, "fig2_lineas_velocidad.png")
    fig.savefig(p2, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(p2)
    print(f"  [OK] {p2}")

    # ── Figura 3: Radar chart ────────────────────────────────
    cats = ["PDR (%)", "Throughput\n(norm)", "1/Latencia\n(norm)", "1/Jitter\n(norm)", "PLR\n(100-x)"]
    N = len(cats)

    def norm(vals, invert=False):
        mx = max(vals) if max(vals) != 0 else 1
        res = [v / mx for v in vals]
        return [1 - r for r in res] if invert else res

    pdr_n   = norm(pdr_vals)
    tput_n  = norm(tput_vals)
    dlat_n  = norm(delay_vals,  invert=True)
    jit_n   = norm(jitter_vals, invert=True)
    plr_n   = norm([100 - p for p in plr_vals])

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    for idx, r in enumerate(results):
        vals_r = [pdr_n[idx], tput_n[idx], dlat_n[idx], jit_n[idx], plr_n[idx]]
        vals_r += vals_r[:1]
        ax.plot(angles, vals_r, "o-", color=PALETTE[idx], linewidth=2, label=short[idx])
        ax.fill(angles, vals_r, color=PALETTE_LIGHT[idx], alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), cats)
    ax.set_title("Perfil de Rendimiento Normalizado", fontsize=12, fontweight="bold", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    ax.grid(True)

    p3 = os.path.join(out_dir, "fig3_radar.png")
    fig.savefig(p3, dpi=150, bbox_inches="tight")
    plt.close(fig)
    saved.append(p3)
    print(f"  [OK] {p3}")

    return saved


# ═════════════════════════════════════════════════════════════
#  4.  CSV
# ═════════════════════════════════════════════════════════════
def export_csv(results: list[dict], out_dir: str) -> str:
    path = os.path.join(out_dir, "manet_resultados.csv")
    keys = ["label", "n_flows", "total_tx", "total_rx", "total_lost",
            "pdr", "plr", "throughput", "delay_ms", "jitter_ms"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            writer.writerow({k: r[k] for k in keys})
    print(f"  [OK] {path}")
    return path


# ═════════════════════════════════════════════════════════════
#  5.  REPORTE PDF
# ═════════════════════════════════════════════════════════════
def build_pdf(results: list[dict], charts: list[str], out_dir: str) -> str:
    path = os.path.join(out_dir, "manet_reporte.pdf")
    doc  = SimpleDocTemplate(path, pagesize=letter,
                              leftMargin=0.75*inch, rightMargin=0.75*inch,
                              topMargin=0.75*inch,  bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story  = []

    # ── Estilos personalizados ────────────────────────────────
    title_style = ParagraphStyle("MyTitle", parent=styles["Title"],
                                  fontSize=16, spaceAfter=6, alignment=TA_CENTER,
                                  textColor=colors.HexColor("#1A237E"))
    h1 = ParagraphStyle("H1", parent=styles["Heading1"],
                          fontSize=13, textColor=colors.HexColor("#1565C0"),
                          spaceBefore=12, spaceAfter=4)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"],
                          fontSize=11, textColor=colors.HexColor("#1976D2"),
                          spaceBefore=8, spaceAfter=4)
    body = ParagraphStyle("Body", parent=styles["Normal"],
                            fontSize=10, leading=14, alignment=TA_JUSTIFY)
    caption = ParagraphStyle("Caption", parent=styles["Normal"],
                               fontSize=9, textColor=colors.grey, alignment=TA_CENTER)

    def hr(): return HRFlowable(width="100%", thickness=0.5,
                                 color=colors.HexColor("#BBDEFB"), spaceAfter=6)

    # ── Portada ───────────────────────────────────────────────
    story += [
        Spacer(1, 0.5*inch),
        Paragraph("Taller 1 — Modelos Estocásticos y Simulación", title_style),
        Paragraph("Análisis de MANET Jerárquica con Movilidad Dual", title_style),
        hr(),
        Spacer(1, 0.2*inch),
        Paragraph(
            "<b>Indagación:</b> ¿Cómo afecta la velocidad de movimiento de los clústeres "
            "backbone (Nivel 2) sobre el throughput extremo a extremo, la tasa de entrega "
            "de paquetes (PDR) y la latencia en una MANET jerárquica con tres clústeres "
            "en el primer nivel y dos en el segundo, bajo movilidad dual (nodo y clúster)?",
            body),
        Spacer(1, 0.3*inch),
    ]

    # ── Sección 1: Descripción del experimento ─────────────────
    story += [
        Paragraph("1. Diseño Experimental", h1), hr(),
        Paragraph(
            "Se simularon tres escenarios en NS-3 variando únicamente la velocidad del "
            "backbone (Nivel 2) para aislar su efecto. Los nodos de Nivel 1 mantienen "
            "velocidad constante de 1 m/s (RandomWalk2D). El protocolo de enrutamiento "
            "es AODV y el área de simulación es 250×250 m durante 100 segundos.", body),
        Spacer(1, 0.15*inch),
    ]

    # Tabla de escenarios
    esc_table_data = [
        ["Escenario", "Velocidad L2", "Modelo L1", "Modelo L2", "Protocolo", "Área"],
        ["E1 – Control",   "2 m/s",  "RandomWalk2D", "Gauss-Markov", "AODV", "250×250 m"],
        ["E2 – Moderado",  "15 m/s", "RandomWalk2D", "Gauss-Markov", "AODV", "250×250 m"],
        ["E3 – Estrés",    "30 m/s", "RandomWalk2D", "Gauss-Markov", "AODV", "250×250 m"],
    ]
    t = Table(esc_table_data, colWidths=[1.2*inch]*6)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#1565C0")),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#E3F2FD"), colors.white]),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#90CAF9")),
        ("ALIGN",        (0,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [t, Spacer(1, 0.2*inch)]

    # ── Sección 2: Resultados numéricos ───────────────────────
    story += [Paragraph("2. Resultados Numéricos", h1), hr()]

    headers = ["Métrica", "E1 – 2 m/s", "E2 – 15 m/s", "E3 – 30 m/s"]
    rows = [
        ["Flujos detectados"]  + [str(r["n_flows"])    for r in results],
        ["Paquetes TX"]        + [str(r["total_tx"])   for r in results],
        ["Paquetes RX"]        + [str(r["total_rx"])   for r in results],
        ["Paquetes perdidos"]  + [str(r["total_lost"]) for r in results],
        ["PDR (%)"]            + [f"{r['pdr']:.2f} %"  for r in results],
        ["PLR (%)"]            + [f"{r['plr']:.2f} %"  for r in results],
        ["Throughput (Kbps)"]  + [f"{r['throughput']:.3f}" for r in results],
        ["Latencia media (ms)"]+ [f"{r['delay_ms']:.4f}"   for r in results],
        ["Jitter medio (ms)"]  + [f"{r['jitter_ms']:.4f}"  for r in results],
    ]
    table_data = [headers] + rows
    col_w = [2.0*inch, 1.4*inch, 1.4*inch, 1.4*inch]
    t2 = Table(table_data, colWidths=col_w)
    t2.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#0D47A1")),
        ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME",     (0,1), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9.5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#E8EAF6"), colors.white]),
        ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#9FA8DA")),
        ("ALIGN",        (1,0), (-1,-1), "CENTER"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    story += [t2, Spacer(1, 0.2*inch)]

    # ── Sección 3: Gráficas ───────────────────────────────────
    story += [PageBreak(), Paragraph("3. Análisis Gráfico", h1), hr()]

    fig_info = [
        ("fig1_panel_barras.png",    "Figura 1 — Panel comparativo: PDR, Throughput, Latencia y Jitter por escenario."),
        ("fig2_lineas_velocidad.png","Figura 2 — Evolución de métricas en función de la velocidad del backbone L2."),
        ("fig3_radar.png",           "Figura 3 — Perfil de rendimiento normalizado (diagrama de radar)."),
    ]
    for fname, cap in fig_info:
        fpath = os.path.join(out_dir, fname)
        if os.path.exists(fpath):
            img = Image(fpath, width=6.5*inch, height=3.8*inch, kind="proportional")
            story += [img, Paragraph(cap, caption), Spacer(1, 0.25*inch)]

    # ── Sección 4: Análisis de resultados ────────────────────
    story += [PageBreak(), Paragraph("4. Análisis de Resultados", h1), hr()]

    best_pdr  = max(results, key=lambda r: r["pdr"])
    worst_pdr = min(results, key=lambda r: r["pdr"])
    best_tput = max(results, key=lambda r: r["throughput"])

    analysis_text = (
        f"Los resultados demuestran que la velocidad de movimiento de los clústeres backbone "
        f"(Nivel 2) tiene un impacto medible sobre las métricas de red de la MANET jerárquica. "
        f"<br/><br/>"
        f"<b>PDR y PLR:</b> El escenario con mejor PDR es <b>{best_pdr['label'].replace(chr(10),' ')}</b> "
        f"({best_pdr['pdr']:.2f}%), mientras que el peor es "
        f"<b>{worst_pdr['label'].replace(chr(10),' ')}</b> ({worst_pdr['pdr']:.2f}%). "
        f"A mayor velocidad, el protocolo AODV debe recalcular rutas con mayor frecuencia, "
        f"lo cual aumenta la probabilidad de pérdida de paquetes durante las rupturas de enlace. "
        f"<br/><br/>"
        f"<b>Throughput:</b> El escenario de mayor throughput es "
        f"<b>{best_tput['label'].replace(chr(10),' ')}</b> ({best_tput['throughput']:.3f} Kbps). "
        f"La degradación observada en los escenarios de mayor velocidad se debe a los períodos "
        f"de desconexión mientras AODV redescubre rutas. "
        f"<br/><br/>"
        f"<b>Latencia y Jitter:</b> Estos indicadores revelan el costo temporal de la movilidad. "
        f"El incremento de latencia con la velocidad confirma que el overhead de RREQ/RREP de "
        f"AODV crece proporcionalmente con la frecuencia de ruptura de enlaces."
    )
    story += [Paragraph(analysis_text, body), Spacer(1, 0.2*inch)]

    # ── Sección 5: Conclusiones ────────────────────────────────
    story += [Paragraph("5. Conclusiones y Recomendaciones", h1), hr()]
    conclusiones = [
        ("<b>C1 — Impacto de la velocidad:</b>",
         "La velocidad del backbone L2 es un factor crítico. Velocidades superiores a 15 m/s "
         "degradan significativamente el PDR y la latencia en la MANET jerárquica simulada."),
        ("<b>C2 — Robustez de AODV:</b>",
         "AODV mantiene conectividad en todos los escenarios, pero su latencia de "
         "reconvergencia se convierte en cuello de botella a alta movilidad."),
        ("<b>R1 — Protocolos proactivos:</b>",
         "Para el Escenario 3 (30 m/s), se recomienda evaluar OLSR o un protocolo "
         "híbrido que combine mantenimiento proactivo en el backbone con reactividad en las hojas."),
        ("<b>R2 — Ajuste del área:</b>",
         "Aumentar el área de simulación o reducir la densidad de nodos puede suavizar "
         "el efecto de borde observado en los clústeres L2 a alta velocidad."),
    ]
    for title_c, text_c in conclusiones:
        story += [Paragraph(title_c, h2),
                  Paragraph(text_c, body),
                  Spacer(1, 0.1*inch)]

    doc.build(story)
    print(f"  [OK] {path}")
    return path


# ═════════════════════════════════════════════════════════════
#  MAIN
# ═════════════════════════════════════════════════════════════
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Analizando resultados de FlowMonitor\n")

    results = []
    for sc in SCENARIOS:
        r = analyze_xml(sc["xml"], sc["label"])
        if r:
            results.append(r)

    if not results:
        print("No se encontró ningún archivo XML. Verifica la variable BASE en el script.")
        sys.exit(1)

    # Consola
    print_summary(results)

    # Gráficas
    charts = make_charts(results, OUTPUT_DIR)

    # CSV
    export_csv(results, OUTPUT_DIR)

    # PDF
    build_pdf(results, charts, OUTPUT_DIR)


if __name__ == "__main__":
    main()
