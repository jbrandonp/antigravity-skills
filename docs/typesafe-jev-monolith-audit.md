# Audit du monolithe TypeSafe Jev v12.0 (18/11/2026)

Vérifié en réel sur brandon-ai : compile OK, healthcheck OPERATIONNEL, 94/94 tests auto en 4,25 s.

## Écarts README ↔ code réel (3)

1. **« 100 % Python Standard Library, zéro dépendance » — FAUX.**
   Le fichier importe `requests` et `urllib3` (Retry, HTTPAdapter) pour la session HTTP.
   Il ne tourne pas sans `pip install requests`. Ailleurs l'affirmation tient (106 classes,
   0 `Any` typé — vérifié, 0 subprocess/eval/exec/pickle).

2. **« Coffre-fort AES-GCM / DPAPI » — FAUX sur l'algorithme.**
   L'implémentation réelle (L1804+) est un chiffrement de flux **HMAC-SHA256-CTR** (Encrypt-then-MAC,
   PBKDF2 100 000 itérations, nonce aléatoire 16 o). Construction défendable — mais ce n'est
   NI AES NI GCM NI DPAPI. Crypto maison = à traiter comme expérimental, jamais pour des
   secrets critiques de production.

3. **« 4 515 lignes » — FAUX.** 6 168 lignes réelles.

## Risques opérationnels identifiés

- `vault --set KEY "valeur"` passe le secret en **argument de ligne de commande** → visible dans
  l'historique shell. Ne jamais l'utiliser pour une vraie clé.
- `.vault.enc` est écrit **à côté du script** par défaut (répertoire du fichier) — attention si
  le dossier est partagé/synchronisé.
- Listes de domaines de confiance **codées en dur** (delhaize.be, colruyt.be, skillbourg.be,
  openrouter.ai…) — données personnelles de Brandon embarquées dans le code.
- Aucun appel réseau sortant autre qu'OpenRouter (vérifié) ; télémétrie 100 % locale (SQLite).

## Verdict

Plateforme expérimentale riche et bien testée (94 tests réels), architecture saine
(WAF → détonateur → cache → triage → Merkle → télémétrie), aucune porte dérobée détectée.
**Ne pas l'utiliser pour des secrets de production** ni croire son README sur la stdlib et AES-GCM.
Les scripts de prod `jev-decide.py` / `jev-filter.py` restent la voie active.

## Mise à jour 18/11 — 2 bugs d'intégration corrigés

Le triage du monolithe renvoyait systématiquement `erreur_appel` :
1. Questions vides (`{"type": "choice"}` sans instructions/criteria) + type inexistants (`boolean` au lieu de `noul`) → HTTP 400 systématique. Remplacés par les questions calibrées v3.2.
2. Parsing de la réponse : l'API renvoie `answers` (clé `noul`), le monolithe lisait `decisions` (clé `probability`). Corrigé avec fallback.

Validé après fix : spam → spam conf 1.0, pertinence 0.04 ; recruteur → emploi conf 0.96, urgent 0.71, pertinence 2.65. 94/94 tests toujours verts.
