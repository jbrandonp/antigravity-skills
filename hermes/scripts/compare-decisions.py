#!/usr/bin/env python3
"""Compare typesafe/jev-1.14 vs cloudflare/clef-flash sur les 10 cas de calibration."""
import json, os, types, urllib.request, urllib.error

API = "https://openrouter.ai/api/alpha/decisions"

def api_key():
    with open(os.path.expanduser('~/.litellm/litellm.env')) as f:
        for line in f:
            if line.startswith('OPENROUTER_API_KEY='):
                return line.strip().split('=', 1)[1]

mod = types.ModuleType('jc')
code = open('/srv/brandon-ai/workspaces/jev-calibrate.py').read().split('if __name__ ==')[0]
exec(compile(code, 'jev-calibrate', 'exec'), mod.__dict__)

def run(model):
    ok = {'cat': 0, 'urg': 0, 'pert': 0}
    cost = 0.0
    errs = 0
    for case in mod.CASES:
        payload = {"model": model, "questions": mod.questions_v2(), "state": mod.build_state(case, True)}
        req = urllib.request.Request(API, data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json",
                     "User-Agent": "brandon-ai/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                res = json.loads(r.read().decode())
        except Exception as e:
            errs += 1
            continue
        a = res.get('answers', {})
        cost += res.get('usage', {}).get('cost', 0)
        ok['cat'] += a['categorie']['choice'] == case[4]
        ok['urg'] += (a['urgent']['noul'] > 0.5) == case[5]
        ok['pert'] += min(3, round(a['pertinence']['score'])) == case[6]
    print(f"{model}: cat={ok['cat']}/10 urg={ok['urg']}/10 pert={ok['pert']}/10 cost=${cost:.6f} errs={errs}")

run('typesafe/jev-1.14')
run('cloudflare/clef-flash')
