# Schéma de Mémoire Persistante : `brand_profile.json` & `voice.md`

Ce fichier définit la structure de persistance pour que Claude conserve la mémoire de votre voix, de vos preuves d'autorité et de votre positionnement d'une session à l'autre sans avoir à répéter vos préférences.

---

## Format JSON (`~/.claude/linkedin/brand_profile.json` ou `brand_profile.json`)

```json
{
  "author": {
    "name": "Brandon",
    "role": "Software Engineer & Builder",
    "location": "Belgium",
    "primary_language": "fr",
    "languages": ["fr", "en"]
  },
  "positioning": {
    "one_liner": "Conception d'architectures logicielles sobres, scrapers haute résilience et exploration du hardware robotique.",
    "proof_points": [
      "Scraper multi-enseignes collectant 140k prix/jour sans proxy payant",
      "Architecture SQLite en production avec latence < 1ms sous forte charge",
      "Auteur du guide open-source awesome-humanoid-hardware-guide"
    ],
    "core_topics": [
      "Web scraping & ingénierie inverse HTTP/TLS",
      "Architecture logicielle sobre & bases de données légères (SQLite)",
      "Robotique humanoïde & contraintes matérielles réelles"
    ],
    "forbidden_topics": [
      "Politique partisane",
      "Conseils de développement personnel creux (mindset, bienveillance)",
      "Spéculation crypto"
    ]
  },
  "style_dna": {
    "tone": "Factuel, direct, sans emphase, centré sur le code et le terrain",
    "spicy_factor": "Spicy (Prend position, critique sans détour les outils surdimensionnés et le bullshit corporate)",
    "sentence_length": "Alternance staccato (phrases courtes de 3-6 mots, explications denses de 15 mots max)",
    "emojis": "Zéro ou 1 maximum par post (jamais en début de chaque puce)",
    "exclamation_marks": 0,
    "em_dashes_max": 1,
    "banned_phrases": [
      "décryptage",
      "incontournable",
      "catalyseur",
      "ce n'est pas seulement X, c'est Y",
      "il ne s'agit pas de X, mais de Y",
      "dans un monde où"
    ]
  },
  "story_bank": [
    {
      "id": "story_01",
      "topic": "Scraping",
      "hook_metric": "0% de blocage sans proxies à 500 €/mois",
      "cost_paid": "4 nuits de debug TLS et d'analyse Wireshark",
      "counter_intuitive_truth": "Les sites bloquent l'ordre des headers HTTP/2 et les ciphers TLS, pas votre IP."
    }
  ]
}
```
