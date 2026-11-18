#!/usr/bin/env python3
"""Extrait le prompt du cron Pipeline et montre les occurrences du chemin de la queue."""
import json

j = json.load(open("/home/arthur/.hermes/cron/jobs.json"))
jobs = j if isinstance(j, list) else j.get("jobs", [])
for x in jobs:
    if x.get("id") == "60302a8c02eb":
        prompt = x.get("prompt", "")
        print("occurrences:", prompt.count("outreach_queue.json"))
        idx = prompt.find("outreach_queue")
        print("contexte:", prompt[max(0, idx-120):idx+60].replace("\n", " "))
        # écrit le prompt pour la mise à jour
        open("/home/arthur/.hermes/cache/scratch/pipeline-prompt.txt", "w").write(
            prompt.replace(
                "/srv/brandon-ai/workspaces/bttp/bttp/03_Vente_et_Prospection_Terrain/outreach_queue.json",
                "/srv/data/bttp-confidentiel/outreach_queue.json"))
        print("prompt corrigé écrit (cache)")
        break