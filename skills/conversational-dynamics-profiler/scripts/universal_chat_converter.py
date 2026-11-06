#!/usr/bin/env python3
"""
universal_chat_converter.py
---------------------------
Universal Conversational Data Ingestion & Sanitization Pipeline.
Ingests raw exports from:
- Meta GDPR JSON (Instagram Direct Messages, Facebook Messenger) with latin1 repairs
- WhatsApp Text Exports (Android/iOS, 12h/24h, multiline support)
- Telegram Desktop JSON exports (result.json)
- Discord Chat Exporter (JSON / CSV)
- Generic JSON, JSONL and standard CSV formats

Normalizes output strictly to `templates/normalized_chat_schema.json`.
Optional PII anonymization engine (--anonymize) for emails, phone numbers, IBANs, and credit cards.

Zero external dependencies - 100% Python 3.10+ standard library.
Strictly typed: Zero 'Any' types in accordance with project standards.
"""

from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import re
import sys
from typing import Dict, List, Optional, Sequence, Tuple, TypedDict, Union


class NormalizedMetadata(TypedDict, total=False):
    platform: str
    duration_seconds: float
    reactions: List[str]


class NormalizedMessage(TypedDict):
    sender: str
    timestamp: str
    text: str
    type: str
    metadata: NormalizedMetadata


PII_PATTERNS: Sequence[Tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), "[EMAIL_REDACTED]"),
    (re.compile(r"\b(?:(?:\+|00)32\s?|0)[1-9](?:[\s.-]?\d{2}){4}\b"), "[PHONE_BE_REDACTED]"),
    (re.compile(r"\b(?:(?:\+|00)33\s?|0)[1-9](?:[\s.-]?\d{2}){4}\b"), "[PHONE_FR_REDACTED]"),
    (re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b"), "[CARD_REDACTED]"),
    (re.compile(r"\b[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){3}(?:[ ]?[0-9]{2})?\b"), "[IBAN_REDACTED]"),
]

COMMON_DATETIME_FORMATS: Sequence[str] = [
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%d/%m/%y %H:%M:%S",
    "%d/%m/%y %H:%M",
    "%m/%d/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M",
    "%m/%d/%y %H:%M:%S",
    "%m/%d/%y %H:%M",
    "%d/%m/%Y %I:%M:%S %p",
    "%d/%m/%Y %I:%M %p",
    "%d/%m/%y %I:%M:%S %p",
    "%d/%m/%y %I:%M %p",
    "%m/%d/%Y %I:%M:%S %p",
    "%m/%d/%Y %I:%M %p",
    "%m/%d/%y %I:%M:%S %p",
    "%m/%d/%y %I:%M %p",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M",
]


def anonymize_text(text: str) -> str:
    """Replaces PII patterns with explicit redaction placeholders."""
    if not text:
        return text
    clean = text
    for pattern, repl in PII_PATTERNS:
        clean = pattern.sub(repl, clean)
    return clean


def parse_datetime_flexible(dt_str: str) -> datetime.datetime:
    """Attempts multiple common datetime formats before falling back to UTC now."""
    cleaned = dt_str.strip().replace("\u202f", " ").replace("\xa0", " ")
    for fmt in COMMON_DATETIME_FORMATS:
        try:
            return datetime.datetime.strptime(cleaned, fmt).replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            continue
    try:
        return datetime.datetime.fromisoformat(cleaned.replace("Z", "+00:00"))
    except ValueError:
        return datetime.datetime.now(datetime.timezone.utc)


class UniversalConverter:

    @staticmethod
    def fix_meta_str(s: str) -> str:
        """Repairs latin-1 mangled UTF-8 text from Meta/Facebook JSON exports."""
        if not s:
            return s
        try:
            return s.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            try:
                return s.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")
            except Exception:
                return s

    @classmethod
    def convert_file(cls, filepath: str, anonymize: bool = False) -> List[NormalizedMessage]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Source file not found: {filepath}")

        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            raw_text = f.read()

        stripped = raw_text.strip()
        if not stripped:
            return []

        # 1. Telegram Desktop result.json
        if stripped.startswith("{") and '"chats"' in stripped and '"messages"' in stripped:
            return cls._parse_telegram_export(raw_text, anonymize)

        # 2. Meta GDPR JSON
        if stripped.startswith("{") and '"messages"' in stripped:
            return cls._parse_meta_json(raw_text, anonymize)

        # 3. Generic JSON list
        if stripped.startswith("["):
            try:
                data = json.loads(raw_text)
                if isinstance(data, list):
                    return cls._parse_generic_json(raw_text, anonymize)
            except Exception:
                pass

        # 4. WhatsApp TXT
        wa_msgs = cls._parse_whatsapp_txt(raw_text, anonymize)
        if wa_msgs:
            return wa_msgs

        # 5. Discord or generic CSV
        lines = stripped.splitlines()
        if lines and ("," in lines[0] or "\t" in lines[0]):
            header_lower = lines[0].lower()
            if "date" in header_lower or "timestamp" in header_lower or "content" in header_lower or "author" in header_lower:
                return cls._parse_csv(raw_text, anonymize)

        # 6. JSONL fallback
        jsonl_msgs = cls._parse_jsonl(raw_text, anonymize)
        if jsonl_msgs:
            return jsonl_msgs

        raise ValueError(f"Could not auto-detect format for: {filepath}")

    @classmethod
    def _parse_meta_json(cls, raw_content: str, anonymize: bool) -> List[NormalizedMessage]:
        data = json.loads(raw_content)
        msgs: List[Dict[str, Union[str, int, float, List[Dict[str, str]]]]] = data.get("messages", [])
        normalized: List[NormalizedMessage] = []

        for m in msgs:
            raw_sender = str(m.get("sender_name", "Unknown"))
            raw_content_str = str(m.get("content", ""))
            sender = cls.fix_meta_str(raw_sender).strip()
            content = cls.fix_meta_str(raw_content_str).strip()
            if anonymize:
                content = anonymize_text(content)

            msg_type = "text"
            if "audio_files" in m:
                msg_type = "voice"
            elif "photos" in m or "videos" in m or "gifs" in m:
                msg_type = "media"
            elif "reactions" in m and not content:
                msg_type = "reaction"
            elif "share" in m:
                msg_type = "share"

            ts_raw = m.get("timestamp_ms", 0)
            ts_ms = float(ts_raw) if isinstance(ts_raw, (int, float)) else 0.0
            dt = datetime.datetime.fromtimestamp(ts_ms / 1000.0, tz=datetime.timezone.utc)

            normalized.append({
                "sender": sender,
                "timestamp": dt.isoformat(),
                "text": content,
                "type": msg_type,
                "metadata": {
                    "platform": "meta"
                }
            })

        normalized.sort(key=lambda x: x["timestamp"])
        return normalized

    @classmethod
    def _parse_telegram_export(cls, raw_content: str, anonymize: bool) -> List[NormalizedMessage]:
        data = json.loads(raw_content)
        msgs: List[Dict[str, Union[str, int, List[Union[str, Dict[str, str]]]]]] = data.get("messages", [])
        if not msgs and "chats" in data:
            chats_dict = data.get("chats", {})
            if isinstance(chats_dict, dict):
                chat_list = chats_dict.get("list", [])
                if chat_list and isinstance(chat_list, list) and isinstance(chat_list[0], dict):
                    msgs = chat_list[0].get("messages", [])

        normalized: List[NormalizedMessage] = []
        for m in msgs:
            sender = str(m.get("from", m.get("actor", "Unknown"))).strip()
            text_val = m.get("text", "")
            if isinstance(text_val, list):
                text_val = "".join(item if isinstance(item, str) else str(item.get("text", "")) for item in text_val)
            content = str(text_val).strip()
            if anonymize:
                content = anonymize_text(content)

            ts_str = str(m.get("date", ""))
            try:
                dt = datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            except Exception:
                dt = datetime.datetime.now(datetime.timezone.utc)

            msg_type = "text"
            if m.get("media_type") == "voice_message":
                msg_type = "voice"
            elif "photo" in m or "file" in m:
                msg_type = "media"

            normalized.append({
                "sender": sender,
                "timestamp": dt.isoformat(),
                "text": content,
                "type": msg_type,
                "metadata": {"platform": "telegram"}
            })

        normalized.sort(key=lambda x: x["timestamp"])
        return normalized

    @classmethod
    def _parse_whatsapp_txt(cls, raw_content: str, anonymize: bool) -> List[NormalizedMessage]:
        pattern1 = re.compile(
            r"^\[?(\d{1,4}[/\-\.]\d{1,2}[/\-\.]\d{2,4})[,\s]+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\]?\s*[-:]?\s*([^:\n]+):\s*(.*)$"
        )
        lines = raw_content.splitlines()
        normalized: List[NormalizedMessage] = []
        curr: Optional[NormalizedMessage] = None

        for line in lines:
            m = pattern1.match(line)
            if m:
                d_str, t_str, sender, txt = m.groups()
                dt_str = f"{d_str} {t_str}"
                dt = parse_datetime_flexible(dt_str)

                content = txt.strip()
                if anonymize:
                    content = anonymize_text(content)

                msg_type = "voice" if "<audio omitted>" in content.lower() or "vocal" in content.lower() else "text"

                curr = {
                    "sender": sender.strip(),
                    "timestamp": dt.isoformat(),
                    "text": content,
                    "type": msg_type,
                    "metadata": {"platform": "whatsapp"}
                }
                normalized.append(curr)
            elif curr:
                extra = "\n" + (anonymize_text(line) if anonymize else line)
                curr["text"] += extra

        normalized.sort(key=lambda x: x["timestamp"])
        return normalized

    @classmethod
    def _parse_generic_json(cls, raw_content: str, anonymize: bool) -> List[NormalizedMessage]:
        items = json.loads(raw_content)
        normalized: List[NormalizedMessage] = []
        if not isinstance(items, list):
            return []

        for item in items:
            if not isinstance(item, dict):
                continue
            sender = str(item.get("sender", item.get("sender_name", "Unknown"))).strip()
            content = str(item.get("text", item.get("content", ""))).strip()
            if anonymize:
                content = anonymize_text(content)

            ts = item.get("timestamp", item.get("timestamp_ms"))
            if isinstance(ts, (int, float)):
                ts_sec = float(ts) / (1000.0 if float(ts) > 1e11 else 1.0)
                dt = datetime.datetime.fromtimestamp(ts_sec, tz=datetime.timezone.utc)
            elif isinstance(ts, str):
                dt = parse_datetime_flexible(ts)
            else:
                dt = datetime.datetime.now(datetime.timezone.utc)

            normalized.append({
                "sender": sender,
                "timestamp": dt.isoformat(),
                "text": content,
                "type": str(item.get("type", "text")),
                "metadata": {"platform": "generic"}
            })

        normalized.sort(key=lambda x: x["timestamp"])
        return normalized

    @classmethod
    def _parse_csv(cls, raw_content: str, anonymize: bool) -> List[NormalizedMessage]:
        lines = raw_content.splitlines()
        delimiter = "\t" if "\t" in lines[0] and "," not in lines[0] else ","
        reader = csv.DictReader(lines, delimiter=delimiter)
        normalized: List[NormalizedMessage] = []

        for row in reader:
            # Case-insensitive row lookup
            row_lower = {k.lower().strip(): v for k, v in row.items() if k}
            sender = row_lower.get("author", row_lower.get("sender", row_lower.get("username", "Unknown"))).strip()
            content = row_lower.get("content", row_lower.get("text", row_lower.get("message", ""))).strip()
            if anonymize:
                content = anonymize_text(content)

            date_val = row_lower.get("date", row_lower.get("timestamp", ""))
            dt = parse_datetime_flexible(date_val) if date_val else datetime.datetime.now(datetime.timezone.utc)

            normalized.append({
                "sender": sender,
                "timestamp": dt.isoformat(),
                "text": content,
                "type": "text",
                "metadata": {"platform": "csv"}
            })

        normalized.sort(key=lambda x: x["timestamp"])
        return normalized

    @classmethod
    def _parse_jsonl(cls, raw_content: str, anonymize: bool) -> List[NormalizedMessage]:
        normalized: List[NormalizedMessage] = []
        for line in raw_content.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            try:
                item = json.loads(line_str)
                if isinstance(item, dict) and ("sender" in item or "sender_name" in item):
                    sender = str(item.get("sender", item.get("sender_name", "Unknown"))).strip()
                    content = str(item.get("text", item.get("content", ""))).strip()
                    if anonymize:
                        content = anonymize_text(content)
                    ts = item.get("timestamp", item.get("timestamp_ms"))
                    if isinstance(ts, (int, float)):
                        ts_sec = float(ts) / (1000.0 if float(ts) > 1e11 else 1.0)
                        dt = datetime.datetime.fromtimestamp(ts_sec, tz=datetime.timezone.utc)
                    elif isinstance(ts, str):
                        dt = parse_datetime_flexible(ts)
                    else:
                        dt = datetime.datetime.now(datetime.timezone.utc)

                    normalized.append({
                        "sender": sender,
                        "timestamp": dt.isoformat(),
                        "text": content,
                        "type": str(item.get("type", "text")),
                        "metadata": {"platform": "jsonl"}
                    })
            except Exception:
                continue
        normalized.sort(key=lambda x: x["timestamp"])
        return normalized


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Universal Conversational Ingestion & Normalizer.")
    parser.add_argument("--input", "-i", type=str, required=True, help="Input export file (Meta JSON, WhatsApp TXT, Telegram, Discord, CSV)")
    parser.add_argument("--output", "-o", type=str, required=True, help="Output normalized canonical JSON file")
    parser.add_argument("--anonymize", "-a", action="store_true", help="Redact emails, phone numbers, IBANs, and credit cards")
    args = parser.parse_args()

    normalized_data = UniversalConverter.convert_file(args.input, anonymize=args.anonymize)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(normalized_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully normalized {len(normalized_data)} messages to: {args.output}")


if __name__ == "__main__":
    main()
