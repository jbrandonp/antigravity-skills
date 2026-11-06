#!/usr/bin/env python3
"""
export_html_dashboard.py
------------------------
Generates an offline, standalone, interactive HTML/SVG visual dashboard from conversational analytics.
Features:
- Pure self-contained HTML/CSS/SVG (Zero external dependencies, zero CDN, 100% offline)
- Health Score Gauge Meter (0-100)
- Gottman Golden Ratio (5:1 Pos/Neg Balance) Indicator
- Bids for Connection Responsiveness Visual Meter
- Volume & Modality Comparative Visualizations
- Hourly Activity Heatmap (24 hours) & Day-of-Week Distribution (7 days)
- Gottman Four Horsemen Threat Radar / Clinical Diagnostic Table
- Linguistic Density & Turn-Taking Entropy Display

Zero external dependencies - 100% Python 3.10+ standard library.
Strictly typed: Zero 'Any' types in accordance with project standards.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List

# Sibling imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_chat_metrics import AnalyticsResult, ChatParser, AdvancedConversationalEngine, CorpusSummary
from generate_relationship_report import RelationshipReportSynthesizer, HealthScoreResult


def generate_html_dashboard(analytics: AnalyticsResult, output_path: str = "") -> str:
    if "error" in analytics:
        err_msg = analytics.get("error", "Erreur d'analyse.")
        html_error = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Conversational Intelligence Dashboard - Erreur</title>
  <style>
    body {{ background: #0f172a; color: #f8fafc; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
    .card {{ background: #1e293b; padding: 2rem; border-radius: 1rem; border: 1px solid #ef4444; text-align: center; max-width: 500px; }}
    h1 {{ color: #ef4444; font-size: 1.5rem; }}
    p {{ color: #94a3b8; margin-top: 1rem; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>⚠️ Corpus Inexploitable</h1>
    <p>{err_msg}</p>
  </div>
</body>
</html>"""
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_error)
        return html_error

    synth = RelationshipReportSynthesizer(analytics)
    health: HealthScoreResult = synth.compute_health_score()
    score = health["score"]
    s: CorpusSummary = analytics.get("summary", {})
    senders: List[str] = s.get("senders", [])
    vol_by_sender: Dict[str, int] = s.get("volume_by_sender", {})
    total_msgs = s.get("total_messages", 0)
    timespan_days = s.get("timespan_days", 0.0)

    # Color tokens
    score_color = "#10b981" if score >= 80 else ("#f59e0b" if score >= 65 else "#ef4444")

    p1 = senders[0] if len(senders) > 0 else "Partenaire 1"
    p2 = senders[1] if len(senders) > 1 else "Partenaire 2"

    # 1. Hourly distribution data (24-Hour circadian bar chart)
    hourly = analytics.get("hourly_distribution", {})
    max_hour_val = 1
    for snd in senders:
        for h in range(24):
            max_hour_val = max(max_hour_val, hourly.get(snd, {}).get(h, 0))

    hourly_svg_bars: List[str] = []
    bar_width = 16.0
    spacing = 26.0
    start_x = 40.0
    chart_height = 110.0
    base_y = 140.0

    for h in range(24):
        x = start_x + (h * spacing)
        v1 = hourly.get(p1, {}).get(h, 0)
        v2 = hourly.get(p2, {}).get(h, 0) if len(senders) > 1 else 0
        h1 = (v1 / max_hour_val) * chart_height
        h2 = (v2 / max_hour_val) * chart_height
        
        y1 = base_y - h1
        y2 = base_y - h2

        hourly_svg_bars.append(f'<rect x="{x}" y="{y1}" width="{bar_width/2 - 1}" height="{h1}" fill="#38bdf8" rx="2"><title>{p1} à {h}h: {v1} msgs</title></rect>')
        if len(senders) > 1:
            hourly_svg_bars.append(f'<rect x="{x + bar_width/2}" y="{y2}" width="{bar_width/2 - 1}" height="{h2}" fill="#ec4899" rx="2"><title>{p2} à {h}h: {v2} msgs</title></rect>')
        hourly_svg_bars.append(f'<text x="{x + bar_width/2}" y="{base_y + 16}" fill="#94a3b8" font-size="10" text-anchor="middle">{h}h</text>')

    hourly_svg = "".join(hourly_svg_bars)

    # 2. Weekday distribution data (7 days)
    weekdays = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    w_data = analytics.get("weekday_distribution", {})
    max_w_val = 1
    for snd in senders:
        for d in weekdays:
            max_w_val = max(max_w_val, w_data.get(snd, {}).get(d, 0))

    weekday_svg_bars: List[str] = []
    w_bar_w = 40.0
    w_spacing = 90.0
    w_start_x = 45.0
    w_base_y = 140.0

    for idx, d_name in enumerate(weekdays):
        x = w_start_x + (idx * w_spacing)
        w_v1 = w_data.get(p1, {}).get(d_name, 0)
        w_v2 = w_data.get(p2, {}).get(d_name, 0) if len(senders) > 1 else 0
        w_h1 = (w_v1 / max_w_val) * chart_height
        w_h2 = (w_v2 / max_w_val) * chart_height

        w_y1 = w_base_y - w_h1
        w_y2 = w_base_y - w_h2

        weekday_svg_bars.append(f'<rect x="{x}" y="{w_y1}" width="{w_bar_w/2 - 2}" height="{w_h1}" fill="#38bdf8" rx="3"><title>{p1} - {d_name}: {w_v1} msgs</title></rect>')
        if len(senders) > 1:
            weekday_svg_bars.append(f'<rect x="{x + w_bar_w/2}" y="{w_y2}" width="{w_bar_w/2 - 2}" height="{w_h2}" fill="#ec4899" rx="3"><title>{p2} - {d_name}: {w_v2} msgs</title></rect>')
        weekday_svg_bars.append(f'<text x="{x + w_bar_w/2}" y="{w_base_y + 18}" fill="#94a3b8" font-size="11" text-anchor="middle">{d_name[:3]}</text>')

    weekday_svg = "".join(weekday_svg_bars)

    # Gottman threats & ratios
    tc = health["threat_counts"]
    v1_cnt = vol_by_sender.get(p1, 0)
    v2_cnt = vol_by_sender.get(p2, 0) if len(senders) > 1 else 0

    p1_rtt = analytics.get("rtt_latency", {}).get(p1, {})
    p2_rtt = analytics.get("rtt_latency", {}).get(p2, {}) if len(senders) > 1 else {}

    g_ratio = s.get("overall_gottman_ratio", 1.0)
    bid_rate = s.get("overall_bid_responsiveness_rate", 0.0)

    html_content = f"""<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Conversational Intelligence Dashboard</title>
  <style>
    :root {{
      --bg-main: #0f172a;
      --bg-card: #1e293b;
      --border-card: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-p1: #38bdf8;
      --accent-p2: #ec4899;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg-main);
      color: var(--text-main);
      padding: 2rem;
      line-height: 1.5;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    .header {{ margin-bottom: 2rem; border-bottom: 1px solid var(--border-card); padding-bottom: 1.5rem; }}
    .title {{ font-size: 1.875rem; font-weight: 700; color: #fff; }}
    .subtitle {{ color: var(--text-muted); font-size: 0.95rem; margin-top: 0.25rem; }}
    
    .grid-metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2rem;
    }}
    .card {{
      background: var(--bg-card);
      border: 1px solid var(--border-card);
      border-radius: 1rem;
      padding: 1.5rem;
    }}
    .card-title {{ font-size: 0.9rem; font-weight: 600; color: var(--text-muted); margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }}
    
    .metric-value {{ font-size: 2.25rem; font-weight: 800; color: #fff; }}
    .metric-sub {{ font-size: 0.875rem; color: var(--text-muted); margin-top: 0.25rem; }}

    .gauge-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    
    .chart-box {{ margin-top: 1.5rem; }}
    .chart-title {{ font-size: 1.125rem; font-weight: 600; margin-bottom: 1rem; }}

    .legend {{ display: flex; gap: 1.5rem; margin-top: 0.75rem; font-size: 0.875rem; }}
    .legend-item {{ display: flex; align-items: center; gap: 0.5rem; }}
    .legend-color {{ width: 12px; height: 12px; border-radius: 3px; }}

    table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.9rem; }}
    th, td {{ padding: 0.75rem; text-align: left; border-bottom: 1px solid var(--border-card); }}
    th {{ color: var(--text-muted); font-weight: 600; }}
    td {{ color: var(--text-main); }}

    .badge {{ display: inline-block; padding: 0.25rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }}
    .badge-success {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
    .badge-warn {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; }}
    .badge-danger {{ background: rgba(239, 68, 68, 0.2); color: #f87171; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 class="title">📊 Conversational Dynamics & Intelligence Dashboard (v8.0)</h1>
      <p class="subtitle">Analyse exhaustive des interactions : <strong>{' vs '.join(senders) if senders else 'N/A'}</strong> | {total_msgs} messages analysés sur {timespan_days} jours</p>
    </div>

    <div class="grid-metrics">
      <!-- Card 1: Health Score -->
      <div class="card gauge-container">
        <div class="card-title">Score de Santé Relationnelle</div>
        <svg width="220" height="120" viewBox="0 0 220 120">
          <path d="M 20 105 A 85 85 0 0 1 200 105" fill="none" stroke="#334155" stroke-width="16" stroke-linecap="round" />
          <path d="M 20 105 A 85 85 0 0 1 200 105" fill="none" stroke="{score_color}" stroke-width="16" stroke-dasharray="267" stroke-dashoffset="{267 - (score / 100.0) * 267}" stroke-linecap="round" />
          <text x="110" y="90" font-size="30" font-weight="bold" fill="#fff" text-anchor="middle">{score}</text>
          <text x="110" y="110" font-size="11" fill="#94a3b8" text-anchor="middle">SUR 100</text>
        </svg>
        <div class="metric-sub" style="font-weight: 600; color: {score_color}; margin-top: 0.25rem;">
          {'🟢 EXCELLENT' if score >= 80 else ('🟡 STABLE' if score >= 65 else '🔴 RISQUE')}
        </div>
      </div>

      <!-- Card 2: Gottman 5:1 Golden Ratio -->
      <div class="card">
        <div class="card-title">Ratio d'Or Gottman (Positif / Négatif)</div>
        <div class="metric-value">{g_ratio} <span style="font-size: 1.25rem; color: var(--text-muted); font-weight: normal;">: 1</span></div>
        <div class="metric-sub">Seuil de stabilité Gottman : <strong>≥ 5.0 : 1</strong></div>
        <div style="margin-top: 0.75rem;">
          <span class="badge {'badge-success' if g_ratio >= 5.0 else ('badge-warn' if g_ratio >= 2.0 else 'badge-danger')}">
            {'🟢 Climat Sécure (≥ 5:1)' if g_ratio >= 5.0 else ('🟡 Zone d\'Alerte (2:1 à 5:1)' if g_ratio >= 2.0 else '🔴 Toxicité / Usure (< 2:1)')}
          </span>
        </div>
      </div>

      <!-- Card 3: Bids for Connection Responsiveness -->
      <div class="card">
        <div class="card-title">Appels de Contact (Bids) Accueillis</div>
        <div class="metric-value">{bid_rate} <span style="font-size: 1.25rem; color: var(--text-muted); font-weight: normal;">%</span></div>
        <div class="metric-sub">Standard Gottman Masters : <strong>≥ 80 %</strong></div>
        <div style="margin-top: 0.75rem;">
          <span class="badge {'badge-success' if bid_rate >= 80.0 else ('badge-warn' if bid_rate >= 50.0 else 'badge-danger')}">
            {'🟢 Haute Réceptivité' if bid_rate >= 80.0 else ('🟡 Réceptivité Moyenne' if bid_rate >= 50.0 else '🔴 Désengagement / Retrait')}
          </span>
        </div>
      </div>

      <!-- Card 4: Volume & Reciprocity -->
      <div class="card">
        <div class="card-title">Volume & Réciprocité</div>
        <div class="metric-value">{total_msgs} <span style="font-size: 1rem; color: var(--text-muted);">messages</span></div>
        <div class="metric-sub">Vélocité : <strong>{s.get('velocity_messages_per_day', 0.0)}</strong> msgs/jour | Entropie H : <strong>{s.get('turn_taking_entropy', 1.0)}</strong></div>
        <div style="margin-top: 1rem;">
          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 0.25rem;">
            <span>{p1} ({v1_cnt})</span>
            <span>{p2 if len(senders)>1 else ''} ({v2_cnt if len(senders)>1 else ''})</span>
          </div>
          <div style="height: 10px; width: 100%; background: #334155; border-radius: 5px; overflow: hidden; display: flex;">
            <div style="width: {round((v1_cnt/max(total_msgs,1))*100, 1)}%; background: var(--accent-p1);"></div>
            <div style="width: {round((v2_cnt/max(total_msgs,1))*100, 1)}%; background: var(--accent-p2);"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chart 1: Hourly Distribution Heatmap -->
    <div class="card chart-box">
      <div class="chart-title">🕒 Rythme Circadien & Distribution Horaire (24 Heures)</div>
      <div style="overflow-x: auto;">
        <svg width="700" height="170" viewBox="0 0 700 170">
          <line x1="30" y1="{base_y}" x2="680" y2="{base_y}" stroke="#334155" stroke-width="1" />
          {hourly_svg}
        </svg>
      </div>
      <div class="legend">
        <div class="legend-item"><div class="legend-color" style="background: var(--accent-p1);"></div><span>{p1}</span></div>
        {f'<div class="legend-item"><div class="legend-color" style="background: var(--accent-p2);"></div><span>{p2}</span></div>' if len(senders)>1 else ''}
      </div>
    </div>

    <!-- Chart 2: Weekday Distribution (7 Days) -->
    <div class="card chart-box">
      <div class="chart-title">📅 Distribution Hebdomadaire (Lundi au Dimanche)</div>
      <div style="overflow-x: auto;">
        <svg width="700" height="170" viewBox="0 0 700 170">
          <line x1="30" y1="{w_base_y}" x2="680" y2="{w_base_y}" stroke="#334155" stroke-width="1" />
          {weekday_svg}
        </svg>
      </div>
      <div class="legend">
        <div class="legend-item"><div class="legend-color" style="background: var(--accent-p1);"></div><span>{p1}</span></div>
        {f'<div class="legend-item"><div class="legend-color" style="background: var(--accent-p2);"></div><span>{p2}</span></div>' if len(senders)>1 else ''}
      </div>
    </div>

    <!-- Gottman & Clinical Breakdown Table -->
    <div class="card chart-box">
      <div class="chart-title">🛡️ Audit Clinique de Gottman & Prévoyance des Risques</div>
      <table>
        <thead>
          <tr>
            <th>Cavalier / Signal d'Alerte</th>
            <th>Occurrence Détectée</th>
            <th>Seuil de Toxicité</th>
            <th>Diagnostic Opérationnel</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Mépris (Contempt)</strong></td>
            <td><code>{tc['contempt']}</code></td>
            <td>0 max</td>
            <td>{'<span class="badge badge-success">Sain (Aucun mépris)</span>' if tc['contempt']==0 else '<span class="badge badge-danger">Alerte Rouge</span>'}</td>
          </tr>
          <tr>
            <td><strong>Critique (Criticism)</strong></td>
            <td><code>{tc['criticism']}</code></td>
            <td>≤ 2</td>
            <td>{'<span class="badge badge-success">Faible / Régulé</span>' if tc['criticism']<=2 else '<span class="badge badge-warn">Surveiller la forme</span>'}</td>
          </tr>
          <tr>
            <td><strong>Défense (Defensiveness)</strong></td>
            <td><code>{tc['defensiveness']}</code></td>
            <td>≤ 3</td>
            <td>{'<span class="badge badge-success">Réparations fluides</span>' if tc['defensiveness']<=3 else '<span class="badge badge-warn">Tendance justification</span>'}</td>
          </tr>
          <tr>
            <td><strong>Dérobade (Stonewalling)</strong></td>
            <td><code>{tc['stonewalling']}</code></td>
            <td>0 max</td>
            <td>{'<span class="badge badge-success">Aucun retrait hostile</span>' if tc['stonewalling']==0 else '<span class="badge badge-warn">Silences prolongés</span>'}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</body>
</html>
"""

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML Dashboard successfully exported to {output_path}")

    return html_content


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Standalone HTML Dashboard Generator for Chat Dynamics.")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to chat export (JSON, WhatsApp TXT, Meta JSON, CSV)")
    parser.add_argument("--output", "-o", type=str, default="dashboard.html", help="Path to output HTML file")
    args = parser.parse_args()

    messages = ChatParser.parse_file(args.input)
    engine = AdvancedConversationalEngine(messages)
    analytics = engine.analyze()

    generate_html_dashboard(analytics, args.output)


if __name__ == "__main__":
    main()
