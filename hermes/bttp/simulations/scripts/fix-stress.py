#!/usr/bin/env python3
"""Correctifs stress tests : enveloppes d'erreur propres + validation BCE mod-97
+ montant positif + import hostile maîtrisé."""
import re

BASE = "/srv/brandon-ai/workspaces/bttp/bttp/05_Outils_et_Modeles_Excel"

def patch_file(path, old, new, label):
    src = open(path, encoding="utf-8").read()
    if old not in src:
        print(f"⚠️ {label}: motif introuvable")
        return
    open(path, "w", encoding="utf-8").write(src.replace(old, new, 1))
    print(f"✅ {label}")

# A. Enveloppe d'erreur propre pour export CSV
p = f"{BASE}/export_devis_to_csv.py"
src = open(p, encoding="utf-8").read()
if "def main() -> None:\n    parser" in src and "_enveloppe_erreur" not in src:
    src = src.replace("def main() -> None:\n    parser",
"""def main() -> None:
    try:
        _main_interne()
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERREUR] {exc}")
        sys.exit(1)
    except Exception as exc:  # classeur corrompu/verrouillé → message propre, pas de traceback
        print(f"[ERREUR] classeur illisible ou verrouillé : {type(exc).__name__}: {exc}")
        sys.exit(1)


def _main_interne() -> None:
    parser""", 1)
    open(p, "w", encoding="utf-8").write(src)
    print("✅ export CSV : enveloppe d'erreur propre")

# B. Enveloppe pour rapport patron
p = f"{BASE}/generate_patron_report.py"
src = open(p, encoding="utf-8").read()
if "def main() -> None:" in src and "_main_interne" not in src:
    src = src.replace("def main() -> None:",
"""def main() -> None:
    try:
        _main_interne()
    except (FileNotFoundError, ValueError) as exc:
        print(f"[ERREUR] {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"[ERREUR] classeur illisible ou verrouillé : {type(exc).__name__}: {exc}")
        sys.exit(1)


def _main_interne() -> None:""", 1)
    # renommer l'appel dans __main__ si présent
    src = src.replace("main()", "_main_interne()", 1) if "__main__" in src else src
    src = src.replace("if __name__ == \"__main__\":\n    _main_interne()",
                      "if __name__ == \"__main__\":\n    main()")
    open(p, "w", encoding="utf-8").write(src)
    print("✅ rapport patron : enveloppe d'erreur propre")

# C. Enveloppe pour relances
p = f"{BASE}/draft_relance_messages.py"
src = open(p, encoding="utf-8").read()
if "def main() -> None:" in src and "_main_interne" not in src:
    src = src.replace("def main() -> None:",
"""def main() -> None:
    try:
        _main_interne()
    except Exception as exc:
        print(f"[ERREUR] classeur illisible ou verrouillé : {type(exc).__name__}: {exc}")
        sys.exit(1)


def _main_interne() -> None:""", 1)
    src = src.replace("if __name__ == \"__main__\":\n    _main_interne()",
                      "if __name__ == \"__main__\":\n    main()")
    open(p, "w", encoding="utf-8").write(src)
    print("✅ relances : enveloppe d'erreur propre")

# D. bttp_import : catch propre dans main
p = f"{BASE}/bttp_import.py"
src = open(p, encoding="utf-8").read()
if "n = import_any(args.source, args.output, args.client_nom)" in src:
    src = src.replace(
        "    n = import_any(args.source, args.output, args.client_nom)",
        """    try:
        n = import_any(args.source, args.output, args.client_nom)
    except (ValueError, FileNotFoundError) as exc:
        print(f"[ERREUR] import refusé : {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"[ERREUR] fichier source illisible : {type(exc).__name__}: {exc}")
        sys.exit(1)""", 1)
    open(p, "w", encoding="utf-8").write(src)
    print("✅ bttp_import : erreurs hostiles maîtrisées")

# E. Peppol : validation BCE mod-97 + montant positif AVANT génération
p = f"{BASE}/generate_peppol_invoice.py"
src = open(p, encoding="utf-8").read()
if "def valider_bce" not in src:
    src = src.replace(
        "def main() -> None:",
"""def valider_bce(cbe: str) -> bool:
    \"\"\"BCE : exactement 10 chiffres (le zfill est interdit — il masquait les BCE invalides).\"\"\"
    return bool(cbe) and cbe.isdigit() and len(cbe) == 10


def avertir_checksum_bce(cbe: str) -> None:
    \"\"\"Avertissement mod-97 NON bloquant : un vrai BCE doit être divisible par 97.\"\"\"
    try:
        if int(cbe) % 97 != 0:
            print(f"⚠️  AVERTISSEMENT : BCE {cbe} — checksum mod-97 non concordant. "
                  f"Vérifiez le numéro auprès de la BCE avant émission.")
    except ValueError:
        pass


def main() -> None:""", 1)
    src = src.replace(
        '    cbe_clean = args.client_cbe.replace(".", "").replace(" ", "").replace("BE", "").zfill(10)',
        """    cbe_clean = args.client_cbe.replace(".", "").replace(" ", "").replace("BE", "")
    if not valider_bce(cbe_clean):
        print(f"[ERREUR] BCE client invalide : '{args.client_cbe}' — exactement 10 chiffres requis")
        sys.exit(1)
    avertir_checksum_bce(cbe_clean)
    if args.amount_htva <= 0:
        print(f"[ERREUR] montant HTVA invalide : {args.amount_htva} — un montant strictement positif est requis")
        sys.exit(1)""", 1)
    open(p, "w", encoding="utf-8").write(src)
    print("✅ Peppol : BCE 10 chiffres + montant positif (rejet propre)")
