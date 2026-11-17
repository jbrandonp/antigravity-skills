# -*- coding: utf-8 -*-
"""Pré-filtre Jev : score de pertinence typé par item.
Modes (stdin) :
  - tableau JSON simple [...items]            → mode "articles" (défaut)
  - {"mode": "findings", "items": [...]}      → findings de sessions (learnings)
  - {"mode": "tenders", "items": [...]}       → appels d'offres
Retourne {total, garder, ecarter, cost, items}. Remplace le scoring GLM pour
les items écartés. Coût : ~$0.00004/item."""
import json, os, sys, urllib.request, urllib.error

API = "https://openrouter.ai/api/alpha/decisions"
MODEL = "typesafe/jev-1.14"
ENV = os.path.expanduser("~/.litellm/litellm.env")

SEUIL_GARDER = 1.5   # score >= 1.5/3 → candidat pour traitement GLM complet
SEUIL_PAR_MODE = {"tenders": 1.3}  # appels d'offres : seuil assoupli (rare, coûteux à rater)

PROFIL = ("Brandon Louis Palhano Machado, 25 ans, Saint-Nicolas (Liège, Belgique). "
          "Étudiant CESS, builder IA (agents autonomes, Hermes, VPS Hetzner, OpenRouter, LiteLLM). "
          "Recherche emploi télétravail administratif/informatique. Intéressé par : IA agents, "
          "dev web, automatisation, sécurité serveur, écosystème start-up, affaires.")

QUESTIONS = {
    "articles": {
        "pertinent": {"type": "score",
                      "criteria": ["0 - Aucun intérêt : people, sport, politique générale, crypto-hype, contenu sponsored.",
                                   "1 - Faible : actualité tech/IA générique, déjà couverte, ou trop niche sans lien avec son quotidien.",
                                   "2 - Utile : avancée IA/agents majeure, outil open-source utilisable, marché emploi tech belge/européen, sécurité serveur, régulation IA.",
                                   "3 - Très pertinent : changement direct pour son stack (agents, LLM APIs, auto-hébergement), opportunité emploi télétravail concret, action possible cette semaine."],
                      "instructions": "Niveau de pertinence de cet article pour Brandon, vu son profil."},
        "action": {"type": "noul",
                   "criteria": {"true": "Brandon peut agir concrètement : tester un outil, postuler, configurer, changer un composant de son stack.",
                                "false": "Simple lecture informative."},
                   "instructions": "Cet article appelle-t-il une action concrète de Brandon ?"},
    },
    "findings": {
        "pertinent": {"type": "score",
                      "criteria": ["0 - Bruit : one-off sans leçon, préférence ponctuelle, info déjà capturée ailleurs.",
                                   "1 - Faible : correction ou préférence mineure, déjà encodable par une simple note existante.",
                                   "2 - Utile : erreur répétée, préférence durable, workaround réutilisable, friction d'outil documentée.",
                                   "3 - Haut signal : correction explicite de Brandon, règle durable, mécanisme à encoder en config/script/skill."],
                      "instructions": "Ce learning issu d'une session mérite-t-il d'être routé (mémoire/skill/config) ?"},
        "action": {"type": "noul",
                   "criteria": {"true": "Encodable structurellement : config, script, skill, cron — pas seulement une note.",
                                "false": "Concerne un cas unique, rien à encoder."},
                   "instructions": "Ce learning est-il encodable en mécanisme durable plutôt qu'en note ?"},
    },
    "tenders": {
        "pertinent": {"type": "score",
                      "criteria": ["0 - Hors sujet : pas BTP/construction, autre région, marché réservé.",
                                   "1 - Faible : BTP Wallonie mais masse de travail incompatible avec un solo (autoroute, hôpital).",
                                   "2 - Utile : travaux/administration compatibles petite structure, région liégeoise.",
                                   "3 - Très pertinent : petite structure admise, Liège/Wallonie, délai réaliste, secteur de Brandon (maintenance, admin, informatique) ou prestation de services."],
                      "instructions": "Cet appel d'offres est-il une piste réaliste pour une micro-structure solo en Wallonie ?"},
        "action": {"type": "noul",
                   "criteria": {"true": "Date limite >= 7 jours et conditions d'accès réalistes pour un solo.",
                                "false": "Délai trop court, conditions restrictives, ou nécessite une équipe."},
                   "instructions": "Cet appel d'offres est-il actionnable dans les délais ?"},
    },
}

def api_key():
    with open(ENV) as f:
        for line in f:
            if line.startswith("OPENROUTER_API_KEY="):
                return line.strip().split("=", 1)[1]
    raise SystemExit("key manquante")

def decide(state, retries=2):
    payload = {"model": MODEL, "questions": QUESTIONS[current_mode()], "state": state}
    headers = {"Authorization": f"Bearer {api_key()}",
               "Content-Type": "application/json",
               "User-Agent": "brandon-ai/1.0"}
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(
                    API, data=json.dumps(payload).encode(), headers=headers), timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries:
                import time; time.sleep(2); continue
            return {"error": e.read().decode()[:150]}
        except Exception:
            if attempt < retries:
                import time; time.sleep(2); continue
            return {"error": "network"}

_mode = "articles"
def current_mode():
    return _mode

def run(items, mode="articles"):
    global _mode
    _mode = mode if mode in QUESTIONS else "articles"
    seuil = SEUIL_PAR_MODE.get(_mode, SEUIL_GARDER)
    results = []
    total_cost = 0.0
    for it in items:
        state = (f"Profil du destinataire : {PROFIL}\n\n"
                 f"Source : {it.get('source','')}\n"
                 f"Titre : {it.get('titre','')}\n"
                 f"Extrait : {(it.get('resume') or it.get('extrait') or '')[:600]}")
        res = decide(state)
        if "error" in res:
            results.append({**it, "erreur": res["error"], "garder": True})  # fail-open
            continue
        a = res["answers"]
        score = a["pertinent"]["score"]
        total_cost += res.get("usage", {}).get("cost", 0)
        results.append({**it, "score_jev": round(score, 2), "action": a["action"]["noul"] > 0.5,
                        "garder": score >= seuil})
    keep = [r for r in results if r.get("garder")]
    out = {"mode": _mode, "total": len(results), "garder": len(keep),
           "ecarter": len(results) - len(keep), "cost": round(total_cost, 6),
           "seuil": seuil, "items": results}
    _mode = "articles"
    return out

if __name__ == "__main__":
    raw = json.loads(sys.stdin.read())
    if isinstance(raw, dict) and "items" in raw:
        items, mode = raw["items"], raw.get("mode", "articles")
    else:
        items, mode = raw, "articles"
    print(json.dumps(run(items, mode), ensure_ascii=False, indent=2))
