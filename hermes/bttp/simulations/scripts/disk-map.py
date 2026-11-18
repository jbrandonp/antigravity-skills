#!/usr/bin/env python3
"""Cartographie du disque système / — top consommateurs."""
import os

def du(path, depth=1):
    total = 0
    for r, d, fs in os.walk(path):
        for f in fs:
            try:
                total += os.path.getsize(os.path.join(r, f))
            except OSError:
                pass
    return total

print("=== Top /srv/brandon-ai ===")
base = "/srv/brandon-ai"
entries = []
for d in os.listdir(base):
    full = os.path.join(base, d)
    if os.path.isdir(full):
        entries.append((d, du(full)))
for d, s in sorted(entries, key=lambda x: -x[1])[:12]:
    print(f"  {s // (1024*1024):>6} Mo  {d}")

print("\n=== Top /home/arthur ===")
home = "/home/arthur"
entries = []
for d in os.listdir(home):
    full = os.path.join(home, d)
    if os.path.isdir(full):
        entries.append((d, du(full)))
for d, s in sorted(entries, key=lambda x: -x[1])[:10]:
    print(f"  {s // (1024*1024):>6} Mo  {d}")

print("\n=== Divers ===")
for p in ("/var/log", "/var/cache", "/tmp", "/var/lib/docker", "/var/lib/snapd"):
    if os.path.exists(p):
        print(f"  {du(p) // (1024*1024):>6} Mo  {p}")
# journald
r = os.popen("sudo -n journalctl --disk-usage 2>/dev/null").read().strip()
print(" ", r)
