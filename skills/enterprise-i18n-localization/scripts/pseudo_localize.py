#!/usr/bin/env python3
"""Enterprise Pseudo-Localization Generator.

Transforms JSON translation key-value catalogs into pseudo-localized test files:
- Replaces ASCII vowels/consonants with accented glyphs (e.g., 'e' -> 'é', 'a' -> 'å')
- Expands string length by ~30% to catch layout clipping and UI container overflow
- Wraps output in bracket markers '[!!! ... !!!]' to instantly expose hardcoded strings
- Preserves ICU MessageFormat variables (e.g., {count}, {name}, %s) untouched
"""

import argparse
import json
from pathlib import Path
import re
import sys

# Mapping table for pseudo-localization characters
GLYPH_MAP = {
    'a': 'å', 'b': 'ƀ', 'c': 'ç', 'd': 'ð', 'e': 'é', 'f': 'ƒ', 'g': 'ĝ',
    'h': 'ĥ', 'i': 'î', 'j': 'ĵ', 'k': 'ķ', 'l': 'ļ', 'm': 'ɱ', 'n': 'ñ',
    'o': 'ô', 'p': 'þ', 'q': 'q', 'r': 'ŕ', 's': 'š', 't': 'ţ', 'u': 'û',
    'v': 'ṽ', 'w': 'ŵ', 'x': 'ẋ', 'y': 'ý', 'z': 'ž',
    'A': 'Å', 'B': 'Ɓ', 'C': 'Ç', 'D': 'Ð', 'E': 'É', 'F': 'Ƒ', 'G': 'Ĝ',
    'H': 'Ĥ', 'I': 'Î', 'J': 'Ĵ', 'K': 'Ķ', 'L': 'Ļ', 'M': 'Ṁ', 'N': 'Ñ',
    'O': 'Ô', 'P': 'Þ', 'Q': 'Q', 'R': 'Ŕ', 'S': 'Š', 'T': 'Ţ', 'U': 'Û',
    'V': 'Ṽ', 'W': 'Ŵ', 'X': 'Ẋ', 'Y': 'Ý', 'Z': 'Ž'
}


def pseudo_transform_string(text: str) -> str:
    # Protect placeholders like {var}, {0}, %s, %d, HTML tags
    tokens = re.split(r"(\{[^}]+\}|<[^>]+>|%[a-zA-Z%])", text)
    transformed_parts = []

    for token in tokens:
        if not token:
            continue
        # If it's a protected token (placeholder or HTML tag), leave it unmodified
        if (token.startswith("{") and token.endswith("}")) or \
           (token.startswith("<") and token.endswith(">")) or \
           (token.startswith("%")):
            transformed_parts.append(token)
        else:
            # Substitute characters
            acc = "".join(GLYPH_MAP.get(ch, ch) for ch in token)
            # Add length expansion (~30% padding)
            if len(acc.strip()) > 3:
                expansion = " " + "·" * max(1, int(len(acc) * 0.3))
                acc = acc + expansion
            transformed_parts.append(acc)

    return f"[!!! {''.join(transformed_parts)} !!!]"


def pseudo_transform_dict(data: dict | list | str) -> dict | list | str:
    if isinstance(data, dict):
        return {k: pseudo_transform_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [pseudo_transform_dict(item) for item in data]
    elif isinstance(data, str):
        return pseudo_transform_string(data)
    else:
        return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Enterprise i18n Pseudo-Localization Generator")
    parser.add_argument("input_file", help="Path to input JSON translation catalog (e.g. en.json)")
    parser.add_argument("-o", "--output", help="Path to output pseudo JSON file (default: stdout or input.pseudo.json)")
    args = parser.parse_args()

    in_path = Path(args.input_file)
    if not in_path.exists():
        print(f"Error: Input file '{in_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        content = json.loads(in_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error: Failed to parse JSON: {e}", file=sys.stderr)
        sys.exit(1)

    pseudo_data = pseudo_transform_dict(content)

    out_json = json.dumps(pseudo_data, ensure_ascii=False, indent=2)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(out_json, encoding="utf-8")
        print(f"✓ Pseudo-localization generated successfully at '{out_path}'")
    else:
        out_path = in_path.with_name(f"{in_path.stem}.pseudo.json")
        out_path.write_text(out_json, encoding="utf-8")
        print(f"✓ Pseudo-localization generated successfully at '{out_path}'")


if __name__ == "__main__":
    main()
