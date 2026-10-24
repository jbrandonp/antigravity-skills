#!/usr/bin/env python3
"""
AI Sales Forecasting Pipeline — Hermes Edition
Based on Scale with Ouss methodology (Oussama Ammar)
Runs weekly, analyzes sales_pipeline table, calculates AI predictions.
"""
import mysql.connector
import json
from datetime import date, timedelta

DB = dict(host='127.0.0.1', port=3306, user='root', password='2108', database='kate_sync')

# Stage → base probability (before AI adjustments)
STAGE_BASELINE = {
    'lead': 10.0, 'qualified': 25.0, 'proposal': 50.0,
    'negotiation': 75.0, 'won': 100.0, 'lost': 0.0
}

# Risk signals that reduce probability
RISK_REDUCTIONS = {
    'no_contact_7d': -15,
    'no_contact_14d': -30,
    'competitor_mentioned': -10,
    'no_decision_maker': -20,
    'negative_sentiment': -15,
    'stagnant_30d': -25
}

def calculate_forecast():
    conn = mysql.connector.connect(**DB)
    c = conn.cursor()

    # Get active deals (not won/lost)
    c.execute("""
        SELECT id, deal_name, stage, amount_eur, engagement_score,
               last_contact_date, days_in_stage, competitor_mentioned,
               decision_maker_contacted
        FROM sales_pipeline
        WHERE stage NOT IN ('won', 'lost')
    """)
    deals = c.fetchall()

    report_lines = []
    total_weighted = 0.0
    alerts = []

    for deal in deals:
        (did, name, stage, amt, eng, last_contact, days_stage,
         competitor, dm_contacted) = deal
        base = STAGE_BASELINE.get(stage, 10.0)
        ajustments = []
        risks = []

        # Check recency
        if last_contact:
            gap = (date.today() - last_contact).days
            if gap > 14:
                base += RISK_REDUCTIONS['no_contact_14d']
                ajustments.append(f'no_contact_14d ({gap}d)')
                risks.append(f'Silence radio: {gap} jours')
            elif gap > 7:
                base += RISK_REDUCTIONS['no_contact_7d']
                ajustments.append(f'no_contact_7d ({gap}d)')
                risks.append(f'Contact perdu: {gap} jours')

        # Stagnant check
        if days_stage and days_stage > 30:
            base += RISK_REDUCTIONS['stagnant_30d']
            ajustments.append(f'stagnant ({days_stage}d)')
            risks.append(f'Stagnation: {days_stage}j dans la même étape')

        # Competitor
        if competitor:
            base += RISK_REDUCTIONS['competitor_mentioned']
            ajustments.append('competitor')
            risks.append('Concurrent mentionné')

        # Decision maker
        if not dm_contacted and stage in ('proposal', 'negotiation'):
            base += RISK_REDUCTIONS['no_decision_maker']
            ajustments.append('no_dm')
            risks.append('Décideur non contacté')

        # Engagement bonus
        if eng and eng > 0.7:
            base += 5
        elif eng and eng < 0.3:
            base -= 10
            risks.append(f'Engagement faible ({eng:.0%})')

        final = max(0, min(100, base))
        weighted = (float(amt) if amt else 0) * (final / 100)
        total_weighted += weighted

        # Update DB
        c.execute("""
            UPDATE sales_pipeline
            SET ai_prediction_score = %s, at_risk_signals = %s, updated_at = NOW()
            WHERE id = %s
        """, (round(final, 1), json.dumps(risks) if risks else None, did))

        status = '🔴' if final < 30 else ('🟡' if final < 60 else '🟢')
        report_lines.append(
            f"{status} **{name}** — {final:.0f}% | {stage} | "
            f"{amt:,.0f}€{' | ⚠️ '+', '.join(risks) if risks else ''}"
        )
        if risks:
            alerts.append(f"⚠️ {name}: {', '.join(risks)}")

    conn.commit()
    conn.close()

    report = f"""📊 **Sales Forecast — {date.today().isoformat()}**

## Pipeline actif
{chr(10).join(report_lines) if report_lines else 'Aucun deal actif'}

## Métriques
- **Deals actifs:** {len(deals)}
- **CA pondéré:** {total_weighted:,.0f}€
- **Forecast Accuracy:** à calibrer (data insuffisante < 3 mois)

## 🚨 Alertes
{chr(10).join(alerts) if alerts else '✅ Aucune alerte'}

---
*AI Forecast v1.0 — basé sur engagement, récence, compétition, décision makers*
"""
    return report

if __name__ == '__main__':
    print(calculate_forecast())
