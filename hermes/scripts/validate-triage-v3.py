#!/usr/bin/env python3
"""Valide le triage v3 (atomic + structured state + confidence routing) sur les 10 cas."""
import importlib.util, json

spec = importlib.util.spec_from_file_location('jd', '/home/arthur/.hermes/scripts/jev-decide.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# 10 cas (catégorie, urgent24h, pertinence) — vérité terrain de la calibration
CASES = [
    ("recruteur@supportyourapp.com", "Invitation entretien support FR/EN à distance",
     "Bonjour, votre candidature a retenu notre attention. Êtes-vous disponible pour un entretien vidéo cette semaine ?",
     "emploi", True, 3),
    ("promo@boutique-x.com", "-70% SUR TOUT CE WEEK-END !!!",
     "Dernière chance ! Profitez de nos soldes flash, cliquez vite !",
     "spam", False, 0),
    ("facturation@basic-fit.be", "Votre prélèvement de ce mois",
     "Nous vous informons du prélèvement de 32,49 EUR pour votre abonnement Basic Fit.",
     "admin", False, 2),
    ("newsletter@arstechnica.com", "AI weekly: new agent frameworks",
     "This week in AI: three new agent orchestration frameworks and an open-source release.",
     "veille", False, 2),
    ("security@paypal.com", "Your account has been limited - verify now",
     "Your account has been suspended. Click here immediately to verify your identity or lose access.",
     "spam", False, 0),
    ("alertes@monitoring.io", "ALERTE: login SSH réussi depuis IP inconnue sur brandon-ai",
     "Nouvelle connexion SSH réussie depuis 185.x.x.x (Russie) sur votre serveur brandon-ai à 03h12.",
     "admin", True, 3),
    ("alex.reed@contractor-hub.com", "Mission Frontend / UI remote 80-100$/h",
     "Suite à votre profil, nous avons une mission freelance frontend remote. Intéressé ?",
     "emploi", True, 3),
    ("digest@linkedin.com", "Votre résumé hebdomadaire LinkedIn",
     "Voici les 10 posts les plus populaires de votre réseau cette semaine.",
     "veille", False, 1),
    ("noreply@famiwal.be", "Versement de votre allocation",
     "Un versement de 548,76 EUR a été effectué sur votre compte le 7 du mois.",
     "admin", False, 2),
    ("growth@saas-tool.io", "Boostez votre business avec l'IA",
     "Notre outil IA révolutionnaire va 10x votre productivité. Essai gratuit, inscrivez-vous maintenant.",
     "spam", False, 0),
]

ok = {"cat": 0, "urg": 0, "pert": 0, "phish": 0}
total_cost = 0.0
escalates = 0
for exp, sujet, corps, cat, urg, pert in CASES:
    r = m.triage_email({"expediteur": exp, "sujet": sujet, "corps": corps})
    total_cost += r["cost"]
    ok["cat"] += r["categorie"] == cat
    ok["urg"] += r["urgent_24h"] == urg
    ok["pert"] += r["haute_pertinence"] == (pert == 3)
    phish_truth = "paypal" in exp or "boutique" in exp
    ok["phish"] += r["phishing"] == phish_truth
    escalates += r["escalate"]
    print(f"{exp[:25]:25s} cat={r['categorie']:6s}({'✓' if r['categorie']==cat else '✗'}) "
          f"urg={str(r['urgent_24h']):5s}({'✓' if r['urgent_24h']==urg else '✗'}) "
          f"pert={r['pertinence']:.2f}({'✓' if r['haute_pertinence']==(pert==3) else '✗'}) "
          f"ph={r['phishing_score']} conf={r['categorie_confiance']:.2f} esc={r['escalate']}")
n = len(CASES)
print(f"\ncat={ok['cat']}/{n} urg={ok['urg']}/{n} haute_pert={ok['pert']}/{n} phish={ok['phish']}/{n}")
print(f"coût total 10 triages (2 appels/email): ${total_cost:.6f} | escalades: {escalates}")
