"""
Auditeur de conformité pour crates Rust 2024.
Vérifie l'absence de paniques non contrôlées (.unwrap() / .expect()),
la présence d'optimisations de profil release (LTO, codegen-units) et les règles Clippy.
"""

from __future__ import annotations
import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class RustCrateAuditResult:
    has_lto_enabled: bool
    has_codegen_units_optimized: bool
    has_no_raw_unwraps: bool
    has_clippy_gates: bool
    score: float
    violations: list[str]


def audit_rust_codebase(cargo_toml_content: str, rust_source_content: str) -> RustCrateAuditResult:
    """Analyse les fichiers Cargo.toml et sources Rust pour valider la robustesse."""
    violations: list[str] = []
    
    # 1. Vérification de Cargo.toml
    has_lto: bool = 'lto = "fat"' in cargo_toml_content or "lto = true" in cargo_toml_content
    has_codegen: bool = "codegen-units = 1" in cargo_toml_content
    has_clippy: bool = "clippy" in cargo_toml_content or "#![deny(clippy" in rust_source_content

    if not has_lto:
        violations.append("LTO (Link-Time Optimization) non activé dans le profil release.")
    if not has_codegen:
        violations.append("codegen-units = 1 non configuré pour la vectorisation maximale.")
    if not has_clippy:
        violations.append("Règles de linting Clippy strictes non déclarées.")

    # 2. Vérification des sources Rust
    unwrap_matches = re.findall(r"\.(unwrap|expect)\s*\(", rust_source_content)
    has_no_unwraps: bool = len(unwrap_matches) == 0

    if not has_no_unwraps:
        violations.append(f"Présence de {len(unwrap_matches)} appels directs à .unwrap() / .expect().")

    total_checks: int = 4
    passed_checks: int = total_checks - len(violations)
    score: float = (passed_checks / total_checks) * 100.0

    return RustCrateAuditResult(
        has_lto_enabled=has_lto,
        has_codegen_units_optimized=has_codegen,
        has_no_raw_unwraps=has_no_unwraps,
        has_clippy_gates=has_clippy,
        score=score,
        violations=violations
    )


def run_self_test() -> int:
    """Valide l'auditeur sur un exemple de code Rust conforme."""
    sample_cargo: str = """
    [package]
    name = "net-engine"
    version = "0.1.0"
    edition = "2024"

    [profile.release]
    opt-level = 3
    lto = "fat"
    codegen-units = 1

    [lints.clippy]
    unwrap_used = "deny"
    """

    sample_rs: str = """
    pub fn parse_header(bytes: &[u8]) -> Result<u32, &'static str> {
        if bytes.len() < 4 {
            return Err("Buffer too short");
        }
        let val = u32::from_be_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]);
        Ok(val)
    }
    """

    result = audit_rust_codebase(sample_cargo, sample_rs)
    print(f"Rust Crate Audit Score: {result.score:.1f}%")
    print(f"LTO Enabled: {result.has_lto_enabled}")
    print(f"Codegen Units Optimized: {result.has_codegen_units_optimized}")
    print(f"No Raw Unwraps: {result.has_no_raw_unwraps}")
    print(f"Clippy Gates: {result.has_clippy_gates}")

    if result.score < 80.0:
        print(f"Audit Rust FAIL: {result.violations}", file=sys.stderr)
        return 1

    print("Audit Rust Crate validé avec succès!")
    return 0


if __name__ == "__main__":
    sys.exit(run_self_test())
