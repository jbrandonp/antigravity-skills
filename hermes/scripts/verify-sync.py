#!/usr/bin/env python3
"""Verify: every local Hermes skill exists in remote repo tree, SKILL.md byte-identical (git blob sha)."""
import os, glob, subprocess

remote = {}
for line in open('/tmp/remote-tree.txt'):
    sha, path = line.strip().split(' ', 1)
    remote[path] = sha

def norm(s):
    return s.lower().replace('-', '').replace('_', '').replace(' ', '')

local = {}
for p in glob.glob('/home/arthur/.hermes/skills/*/SKILL.md'):
    d = os.path.dirname(p)
    local[norm(os.path.basename(d))] = (os.path.basename(d), d)

missing, verified, mismatched = [], 0, []
for key, (name, d) in sorted(local.items()):
    candidates = [path for path in remote if path.endswith('/SKILL.md') and norm(path.split('/')[-2]) == key]
    if not candidates:
        missing.append(name)
        continue
    sha = subprocess.run(['git', 'hash-object', os.path.join(d, 'SKILL.md')], capture_output=True, text=True).stdout.strip()
    if any(remote[c] == sha for c in candidates):
        verified += 1
    else:
        mismatched.append(name)

print(f"local skills: {len(local)} | verified byte-identical: {verified}")
print(f"MISSING in repo: {len(missing)}: {missing}")
print(f"CONTENT DIFFERS: {len(mismatched)}: {mismatched}")
