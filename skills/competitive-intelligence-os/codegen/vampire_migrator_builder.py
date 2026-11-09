"""
Générateur autonome d'armes de migration logicielle ('Attaque Vampire').
Synthétise automatiquement un script Python permettant d'importer les fichiers
d'export d'un concurrent (CSV/Excel) directement dans notre base de données locale.
Réduit le coût de transfert (Switching Cost) du client à zéro.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ColumnMapping:
    source_column: str
    target_field: str
    data_type: str  # 'str', 'float', 'date'


@dataclass(frozen=True)
class VampireMigratorSpec:
    competitor_name: str
    supported_format: str  # 'CSV', 'XLSX'
    delimiter: str
    mappings: list[ColumnMapping]


class VampireMigratorBuilder:
    """Générateur de code Python pour scripts de migration 1-clic."""

    @classmethod
    def generate_python_script(cls, spec: VampireMigratorSpec) -> str:
        """Produit le code source complet du script de migration prêt à l'emploi."""
        table_name = f"imported_{spec.competitor_name.lower().replace(' ', '_')}"
        col_defs = ", ".join(f"{m.target_field} {'REAL' if m.data_type == 'float' else 'TEXT'}" for m in spec.mappings)
        placeholders = ", ".join("?" for _ in spec.mappings)
        target_fields = ", ".join(m.target_field for m in spec.mappings)

        lines: list[str] = [
            '"""',
            f"Script de migration automatique depuis {spec.competitor_name}.",
            "Généré automatiquement par le skill competitive-intelligence-os.",
            '"""',
            "",
            "import csv",
            "import sqlite3",
            "from pathlib import Path",
            "from typing import List, Dict",
            "",
            f"def migrate_from_{spec.competitor_name.lower().replace(' ', '_')}(source_file: Path, target_db: Path) -> int:",
            f'    """Parse l\'export {spec.supported_format} de {spec.competitor_name} et injecte dans SQLite."""',
            "    count = 0",
            "    conn = sqlite3.connect(target_db)",
            "    with conn:",
            f'        conn.execute("CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col_defs});")',
            "",
            '    with open(source_file, "r", encoding="utf-8-sig") as f:',
            f'        reader = csv.DictReader(f, delimiter="{spec.delimiter}")',
            "        with conn:",
            "            for row in reader:",
        ]

        # Logique de parsing
        vals: list[str] = []
        for m in spec.mappings:
            if m.data_type == "float":
                lines.append(f'                val_{m.target_field} = float(row.get("{m.source_column}", 0.0) or 0.0)')
            else:
                lines.append(f'                val_{m.target_field} = str(row.get("{m.source_column}", "")).strip()')
            vals.append(f"val_{m.target_field}")

        vals_tuple = f"({', '.join(vals)})" if len(vals) > 1 else f"({vals[0]},)"
        lines.append(f'                conn.execute("INSERT INTO {table_name} ({target_fields}) VALUES ({placeholders});", {vals_tuple})')
        lines.extend([
            "                count += 1",
            "    conn.close()",
            f'    print(f"[OK] {{count}} enregistrements migrés avec succès depuis {spec.competitor_name}.")',
            "    return count",
        ])

        return "\n".join(lines)

    @classmethod
    def export_script_file(cls, spec: VampireMigratorSpec, output_file: Path) -> Path:
        """Génère et sauvegarde le fichier de migration Python sur le disque."""
        code = cls.generate_python_script(spec)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(code, encoding="utf-8")
        return output_file
