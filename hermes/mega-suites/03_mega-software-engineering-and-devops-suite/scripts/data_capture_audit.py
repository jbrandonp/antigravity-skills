#!/usr/bin/env python3
"""
data_capture_audit.py — Audit anti-oubli des données Brandon (Kate 🖤)
============================================================
Vérifie que TOUTES les sources de données personnelles de Brandon sont bien
capturées (logs du jour, chroniques PDT, vault) et détecte les trous.

Sortie : rapport compact (0 ligne si tout est OK → cron SILENT, sinon alerte).

Usage :
  python data_capture_audit.py              # audit complet
  python data_capture_audit.py --verbose    # rapport détaillé
"""
import os, sys, json, datetime, subprocess

HOME = "C:/Users/brand"
LOGS_DIR = os.path.join(HOME, "cogni-self/logs")
CHRON_DIR = os.path.join(HOME, "Obsidian_Vault/03_Timeline")
TWIN_CHRON = os.path.join(HOME, "OneDrive/Documents/Obsidian Vault/Personal_Twin/Chroniques")
VAULT_DIR = os.path.join(HOME, "Obsidian_Vault")

VERBOSE = "--verbose" in sys.argv

def today():
    return datetime.date.today().isoformat()

def main():
    issues = []
    info = []
    today_str = today()

    # 1. Logs Cogni-Self du jour
    today_log = os.path.join(LOGS_DIR, f"activity-{today_str}.jsonl")
    if not os.path.exists(today_log):
        issues.append(f"⚠️ PAS de log Cogni-Self pour aujourd'hui ({today_str}) — le logger ne tourne pas ou le rollover est cassé")
    else:
        size = os.path.getsize(today_log)
        info.append(f"✅ Log du jour: {size/1024:.0f} KB")
        # Vérifier que le fichier est récent (écrit dans les 2 dernières heures)
        mtime = os.path.getmtime(today_log)
        age_h = (datetime.datetime.now().timestamp() - mtime) / 3600
        if age_h > 2:
            issues.append(f"⚠️ Log du jour vieux de {age_h:.1f}h — le logger semble figé (fichier: {os.path.basename(today_log)})")

    # 2. Vérifier le rollover (le log d'hier ne doit JAMAIS grossir après minuit)
    #    Test robuste : comparer la taille sur 2 lectures espacées — pas l'âge (faux positifs)
    prev = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    prev_log = os.path.join(LOGS_DIR, f"activity-{prev}.jsonl")
    if os.path.exists(prev_log):
        size1 = os.path.getsize(prev_log)
        import time as _t
        _t.sleep(3)
        size2 = os.path.getsize(prev_log)
        if size2 > size1:
            issues.append(f"⚠️ ROLLOVER CASSÉ: le log d'hier ({prev}) GROSSIT encore (+{size2-size1} o en 3s) — un vieux logger écrit dans le mauvais fichier")

    # 3. Chronique PDT du jour (ingest 23h30)
    chron_day = os.path.join(TWIN_CHRON, "2026", f"{today_str}.md")
    if not os.path.exists(chron_day):
        info.append(f"ℹ️ Chronique PDT du jour pas encore créée (ingest à 23h30 — normal si avant minuit)")

    # 4. Fichiers vault récents (activité)
    vault_recent = 0
    cutoff = datetime.datetime.now().timestamp() - 7 * 86400
    for root, dirs, files in os.walk(VAULT_DIR):
        if ".obsidian" in root: continue
        for f in files:
            if f.endswith(".md"):
                p = os.path.join(root, f)
                if os.path.getmtime(p) > cutoff:
                    vault_recent += 1
    info.append(f"✅ {vault_recent} fichiers vault modifiés sur 7 jours")

    # 5. Daemon logger actif ?
    try:
        r = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=20, encoding="cp1252", errors="replace")
        if "activity_logger" not in r.stdout and "python" not in r.stdout.lower():
            issues.append("⚠️ Aucun processus python détecté — le logger Cogni-Self est peut-être arrêté")
    except Exception:
        pass

    # 6. Mémoire Hermes taille (saine ?)
    mem_path = os.path.join(HOME, "AppData/Local/hermes/memories/MEMORY.md")
    user_path = os.path.join(HOME, "AppData/Local/hermes/memories/USER.md")
    for p, name, limit in [(mem_path, "MEMORY.md", 176000), (user_path, "USER.md", 110000)]:
        if os.path.exists(p):
            sz = os.path.getsize(p)
            pct = 100 * sz / limit
            if pct > 85:
                issues.append(f"⚠️ {name} à {pct:.0f}% de sa limite ({sz/1024:.0f} KB) — consolidation nécessaire")
            else:
                info.append(f"✅ {name}: {sz/1024:.0f} KB ({pct:.0f}%)")

    # Sortie
    if VERBOSE:
        print("\n".join(info))
        print("\n".join(issues) if issues else "\n✅ Aucun problème")
    else:
        if issues:
            print("\n".join(issues))
            print(f"[{today_str} {datetime.datetime.now().strftime('%H:%M')}]")

if __name__ == "__main__":
    main()
