#!/usr/bin/env python3
"""Vérifie que le schéma crm est intact après la migration du data_directory."""
import subprocess

dbs = subprocess.run(["sudo", "-n", "-u", "postgres", "psql", "-tAc",
                      "SELECT datname FROM pg_database WHERE NOT datistemplate;"],
                     capture_output=True, text=True).stdout.split()
for db in dbs:
    r = subprocess.run(["sudo", "-n", "-u", "postgres", "psql", "-d", db, "-tAc",
                        "SELECT count(*) FROM information_schema.tables WHERE table_schema='crm';"],
                       capture_output=True, text=True)
    if r.stdout.strip() and r.stdout.strip() != "0":
        n_contacts = subprocess.run(["sudo", "-n", "-u", "postgres", "psql", "-d", db, "-tAc",
                                     "SELECT count(*) FROM crm.contacts;"],
                                    capture_output=True, text=True).stdout.strip()
        print(f"CRM trouvé dans la base '{db}': {r.stdout.strip()} tables, {n_contacts} contacts ✓")
    else:
        print(f"base '{db}': pas de schéma crm")
