# Rapport d'audit sécurité — havolib

**Date :** 2026-08-14 12:24 UTC · **Périmètre :** `C:\Users\brand\havok-toolbox\havolib`

| Scanner | Verdict | Détail |
|---------|---------|--------|
| gitleaks | 🟢 OK |  |
| semgrep | 🔴 FINDINGS | 3 findings: |
| osv | 🔴 FINDINGS | Scanning dir C:\Users\brand\havok-toolbox\havolib |

## gitleaks — OK
```

    ○
    │╲
    │ ○
    ○ ░
    ░    gitleaks

[90m2:23PM[0m [32mINF[0m [1mscanned ~1774860 bytes (1.77 MB) in 521ms[0m
[90m2:23PM[0m [32mINF[0m [1mno leaks found[0m

```

## semgrep — FINDINGS
```
3 findings:
[ERROR] ./config.py:200 (python37-compatibility-importlib2) Found 'importlib.resources', which is a module only available on Python 3.7+. This does not work in lower versions, and therefore is not backwards compatible. Use importlib_resources instead for older
[ERROR] ./data_loader.py:27 (python37-compatibility-importlib2) Found 'importlib.resources', which is a module only available on Python 3.7+. This does not work in lower versions, and therefore is not backwards compatible. Use importlib_resources instead for older
[WARNING] ./models/_utils.py:14 (non-literal-import) Untrusted user input in `importlib.import_module()` function allows an attacker to load arbitrary code. Avoid dynamic values in `importlib.import_module()` or use a whitelist to prevent running untrus
```

## osv — FINDINGS
```
Scanning dir C:\Users\brand\havok-toolbox\havolib
Starting filesystem walk for root: C:\
End status: 11 dirs visited, 66 inodes visited, 0 Extract calls, 10.6894ms elapsed, 10.6894ms wall time
No package sources found, --help for usage information.

```
