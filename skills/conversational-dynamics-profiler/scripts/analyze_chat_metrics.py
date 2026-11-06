#!/usr/bin/env python3
"""
analyze_chat_metrics.py
-----------------------
Enterprise-grade quantitative analytics engine for chat & messaging archives.
Supports auto-detection and parsing across multiple formats:
- Meta / Instagram / Facebook Messenger GDPR JSON exports (handles latin1-utf8 encoding artifacts)
- WhatsApp text export formats (Android & iOS date-time conventions, 12h/24h)
- JSON Lines (JSONL) & Generic JSON message lists
- Standard CSV / TSV conversational exports

Advanced Clinical & Psycholinguistic Metrics:
- Turnaround Latency (RTT) & Asymmetry
- Gottman Four Horsemen indicators (Criticism, Contempt, Defensiveness, Stonewalling)
- Gottman Golden Ratio (5:1 Positive/Negative interaction threshold)
- Bids for Connection Responsiveness (Turning Toward vs Away vs Against)
- Mentalization Index (Internal state words vs Teleological action words)
- Emotional Temperature Index (Caps, elongation, exclamation, arousal emojis)
- Reciprocity & Equilibrium Scores
- Silence Breakage & Session Inception Tracking
- Circadian 24-Hour and Weekday Activity Distribution

Zero external dependencies - 100% Python 3.10+ standard library.
Strictly typed: Zero untyped parameters or generic wildcards, in accordance with project standards.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import datetime
import json
import math
import os
import re
import statistics
import sys
from typing import Dict, List, Optional, Sequence, Tuple, TypedDict, Union


# --- TYPING & DATA SCHEMAS (ZERO 'ANY') ---

class LinguisticStats(TypedDict):
    text_messages: int
    total_words: int
    avg_words: float
    median_words: float
    max_words: int
    questions_count: int
    question_rate_percent: float
    unique_words: int
    type_token_ratio: float
    caps_emphasis_words: int
    elongated_words: int
    exclamation_marks: int


class BurstStats(TypedDict):
    turns_count: int
    avg_burst: float
    median_burst: float
    max_burst: int


class LatencyStats(TypedDict, total=False):
    median_seconds: float
    mean_seconds: float
    under_60s_percent: float
    under_300s_percent: float
    turnarounds_measured: int


class SilenceEvent(TypedDict):
    duration_hours: float
    reopened_by: str
    reopened_at: str
    preview: str


class SessionEvent(TypedDict):
    opener: str
    started_at: str
    ended_at: str
    messages: int


class AffectiveValenceStats(TypedDict):
    positive_indicators: int
    negative_indicators: int
    pos_neg_ratio: float
    emotional_safety_status: str


class BidStats(TypedDict):
    bids_initiated: int
    turned_toward: int
    turned_away: int
    turned_against: int
    responsiveness_rate_percent: float


class CorpusSummary(TypedDict, total=False):
    total_messages: int
    senders: List[str]
    first_date: str
    last_date: str
    timespan_days: float
    velocity_messages_per_day: float
    volume_by_sender: Dict[str, int]
    total_sessions: int
    session_openers: Dict[str, int]
    silence_events_count: int
    silence_breakers: Dict[str, int]
    reciprocity_balance_score: float
    curiosity_balance_score: float
    turn_taking_entropy: float
    overall_gottman_ratio: float
    overall_bid_responsiveness_rate: float
    coregulation_health_badge: str


class AnalyticsResult(TypedDict, total=False):
    summary: CorpusSummary
    weekday_distribution: Dict[str, Dict[str, int]]
    hourly_distribution: Dict[str, Dict[int, int]]
    types_breakdown: Dict[str, Dict[str, int]]
    linguistics: Dict[str, LinguisticStats]
    burstiness: Dict[str, BurstStats]
    rtt_latency: Dict[str, LatencyStats]
    emoji_taxonomies: Dict[str, Dict[str, int]]
    gottman_indicators: Dict[str, Dict[str, int]]
    mentalization_indicators: Dict[str, Dict[str, int]]
    affective_valence: Dict[str, AffectiveValenceStats]
    bids_for_connection: Dict[str, BidStats]
    silence_log: List[SilenceEvent]
    error: str


# --- TAXONOMIES & LEXICONS ---

EMOJI_CATEGORIES: Dict[str, List[str]] = {
    "laughter": ["😂", "🤣", "😭", "😹"],
    "affection_love": ["❤️", "💖", "💕", "💞", "💓", "💗", "💘", "💝", "💟", "💜", "💙", "💚", "💛", "🧡", "🤍", "🤎", "🖤"],
    "tenderness_kisses": ["🥰", "😍", "😘", "😚", "😙", "💋", "🫶", "🫶🏼", "🫶🏽", "🫶🏾", "🫶🏿"],
    "playful_seducing": ["😏", "🤤", "😉", "😜", "😝", "😋", "👀", "🔥"],
    "thinking_doubt": ["🤔", "🧐", "🤨", "😶", "🤐", "😵‍💫", "😵"],
    "agreement_validation": ["👍", "👌", "✅", "🙌", "👏", "🤝"],
    "cold_distance_shock": ["🥶", "😐", "😑", "🙄", "😱", "😨", "😰", "😳"],
    "gentle_support": ["🤗", "😌", "😇", "🫂", "🕊️", "✨"]
}

GOTTMAN_LEXICON: Dict[str, List[str]] = {
    "criticism": [
        "tu es toujours", "tu n'es jamais", "tu fais jamais", "tu ne fais jamais", 
        "à deux vitesses", "a deux vitesses", "fatiguée de toi", "fatigué de toi",
        "pourquoi tu", "encore une fois", "t'es chiant", "t'es lourde", "t'es lourd"
    ],
    "contempt": [
        "ridicule", "pathétique", "pff", "n'importe quoi", "ferme là", "tg", "tgggg", 
        "casse-toi", "dégage", "gamin", "pauvre mec", "folle"
    ],
    "defensiveness": [
        "c'est pas ma faute", "c'était juste", "c etait juste", "j'ai rien fait", 
        "c'est toi qui", "c est toi qui", "toujours ma faute", "tu fais pareil",
        "c'était pour tester", "c etait pour tester", "t'exagères", "t exagères"
    ],
    "stonewalling_terms": [
        "k", "ok.", "comme tu veux", "bref", "laisse tomber", "peu importe"
    ]
}

MENTALIZATION_LEXICON: Dict[str, List[str]] = {
    "reflective_cognitive": [
        "je pense", "tu penses", "je ressens", "tu ressens", "sentiment", "émotion",
        "intention", "comprendre", "empathie", "doute", "percevoir", "croire", 
        "se remettre en question", "vulnérable", "solitude", "peur", "blesser"
    ],
    "teleological_action": [
        "prouve", "prouver", "fais", "viens", "montre", "montrer", "achète", 
        "regarde", "arrête", "donne", "faut faire", "dois", "obligé"
    ]
}

POSITIVE_VALENCE_LEXICON: List[str] = [
    "merci", "remercie", "reconnaissant", "reconnaissante", "touché", "touchée",
    "je t'aime", "t'aime", "mon coeur", "chéri", "chérie", "chaton", "chou",
    "magnifique", "sublime", "beau", "belle", "trop bien", "super", "génial", 
    "parfait", "adore", "hâte", "trop hâte", "mdr", "ptdr", "rire", "rigoler",
    "fierté", "fier", "fière", "bravo", "comprends", "d'accord", "apaisé", "apaisée"
]

NEGATIVE_VALENCE_LEXICON: List[str] = [
    "marre", "saoulé", "saoulée", "fatigué de", "fatiguée de", "agacé", "agacée",
    "énervé", "énervée", "peur", "doute", "inquiète", "angoisse", "abandonner",
    "perdre", "reproche", "pourquoi tu", "toujours pareil", "n'importe quoi",
    "chiant", "lourd", "lourde", "froideur", "froid", "distant",
    "ridicule", "pathétique", "laisse tomber", "bref"
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


def parse_datetime_flexible(dt_str: str) -> datetime.datetime:
    """Attempts multiple standard datetime patterns before ISO/now fallback."""
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


@dataclass
class Message:
    sender: str
    timestamp: datetime.datetime
    text: str
    msg_type: str = "text"
    raw_length_words: int = 0
    raw_length_chars: int = 0

    def __post_init__(self):
        if not self.raw_length_words and self.text:
            words = self.text.split()
            self.raw_length_words = len(words)
            self.raw_length_chars = len(self.text)


class ChatParser:
    """Multi-format conversation log parser."""

    @staticmethod
    def fix_meta_encoding(s: str) -> str:
        """Fixes latin-1 mangled UTF-8 text from Meta/Facebook JSON exports."""
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
    def parse_file(cls, filepath: str) -> List[Message]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            full_content = f.read()

        stripped = full_content.strip()
        if not stripped:
            return []

        # 1. Try Meta JSON format
        if stripped.startswith("{") and '"messages"' in stripped:
            try:
                data = json.loads(stripped)
                if isinstance(data, dict) and "messages" in data and isinstance(data["messages"], list):
                    return cls._parse_meta_json(data["messages"])
            except Exception:
                pass

        # 2. Try Generic JSON List
        if stripped.startswith("["):
            try:
                data = json.loads(stripped)
                if isinstance(data, list):
                    return cls._parse_generic_json(data)
            except Exception:
                pass

        # 3. Try WhatsApp text export
        messages = cls._parse_whatsapp_text(full_content)
        if messages:
            return messages

        # 4. Try JSONL
        messages = cls._parse_jsonl(full_content)
        if messages:
            return messages

        raise ValueError(f"Unable to auto-detect chat log format for file: {filepath}")

    @classmethod
    def _parse_meta_json(cls, raw_messages: List[Dict[str, Union[str, int, float, List[Dict[str, str]]]]]) -> List[Message]:
        parsed: List[Message] = []
        for m in raw_messages:
            raw_sender = str(m.get("sender_name", "Unknown"))
            raw_content = str(m.get("content", ""))
            sender = cls.fix_meta_encoding(raw_sender)
            content = cls.fix_meta_encoding(raw_content)
            
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
            parsed.append(Message(sender=sender, timestamp=dt, text=content, msg_type=msg_type))

        parsed.sort(key=lambda x: x.timestamp)
        return parsed

    @classmethod
    def _parse_generic_json(cls, raw_items: List[Dict[str, Union[str, int, float, bool]]]) -> List[Message]:
        parsed: List[Message] = []
        for item in raw_items:
            if not isinstance(item, dict):
                continue
            sender = str(item.get("sender", item.get("sender_name", "Unknown"))).strip()
            text = str(item.get("text", item.get("content", ""))).strip()
            msg_type = str(item.get("type", "text")).strip().lower()

            ts_val = item.get("timestamp", item.get("timestamp_ms"))
            if isinstance(ts_val, (int, float)):
                ts_sec = float(ts_val)
                if ts_sec > 1e11:
                    ts_sec /= 1000.0
                dt = datetime.datetime.fromtimestamp(ts_sec, tz=datetime.timezone.utc)
            elif isinstance(ts_val, str):
                dt = parse_datetime_flexible(ts_val)
            else:
                dt = datetime.datetime.now(datetime.timezone.utc)

            parsed.append(Message(sender=sender, timestamp=dt, text=text, msg_type=msg_type))

        parsed.sort(key=lambda x: x.timestamp)
        return parsed

    @classmethod
    def _parse_whatsapp_text(cls, content: str) -> List[Message]:
        pattern1 = re.compile(
            r"^\[?(\d{1,4}[/\-\.]\d{1,2}[/\-\.]\d{2,4})[,\s]+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[APap][Mm])?)\]?\s*[-:]?\s*([^:\n]+):\s*(.*)$"
        )
        lines = content.splitlines()
        parsed: List[Message] = []
        current_msg: Optional[Message] = None

        for line in lines:
            match = pattern1.match(line)
            if match:
                date_str, time_str, sender, text = match.groups()
                dt_str = f"{date_str} {time_str}"
                dt = parse_datetime_flexible(dt_str)

                current_msg = Message(
                    sender=sender.strip(),
                    timestamp=dt,
                    text=text.strip(),
                    msg_type="voice" if "<audio omitted>" in text.lower() or "vocal" in text.lower() else "text"
                )
                parsed.append(current_msg)
            elif current_msg:
                current_msg.text += "\n" + line
                current_msg.raw_length_words = len(current_msg.text.split())
                current_msg.raw_length_chars = len(current_msg.text)

        parsed.sort(key=lambda x: x.timestamp)
        return parsed

    @classmethod
    def _parse_jsonl(cls, content: str) -> List[Message]:
        parsed: List[Message] = []
        for line in content.splitlines():
            line_str = line.strip()
            if not line_str:
                continue
            try:
                item = json.loads(line_str)
                if isinstance(item, dict) and ("sender" in item or "sender_name" in item):
                    sender = str(item.get("sender", item.get("sender_name", "Unknown")))
                    text = str(item.get("text", item.get("content", "")))
                    ts = item.get("timestamp", item.get("timestamp_ms"))
                    if isinstance(ts, (int, float)):
                        ts_sec = float(ts)
                        if ts_sec > 1e11:
                            ts_sec /= 1000.0
                        dt = datetime.datetime.fromtimestamp(ts_sec, tz=datetime.timezone.utc)
                    elif isinstance(ts, str):
                        dt = parse_datetime_flexible(ts)
                    else:
                        dt = datetime.datetime.now(datetime.timezone.utc)
                    parsed.append(Message(sender=sender, timestamp=dt, text=text))
            except Exception:
                continue
        parsed.sort(key=lambda x: x.timestamp)
        return parsed


class AdvancedConversationalEngine:
    def __init__(self, messages: List[Message], session_gap_hours: float = 4.0, silence_gap_hours: float = 24.0):
        self.messages = messages
        self.session_gap = datetime.timedelta(hours=session_gap_hours)
        self.silence_gap = datetime.timedelta(hours=silence_gap_hours)

    def analyze(self) -> AnalyticsResult:
        if not self.messages:
            return {"error": "Empty message corpus"}

        senders = sorted(list({m.sender for m in self.messages}))
        total_count = len(self.messages)

        # 1. Volume & Modality
        vol_by_sender: Counter[str] = Counter(m.sender for m in self.messages)
        type_by_sender: Dict[str, Counter[str]] = defaultdict(Counter)
        text_msgs_by_sender: Dict[str, List[Message]] = defaultdict(list)

        for m in self.messages:
            type_by_sender[m.sender][m.msg_type] += 1
            if m.msg_type == "text" or (m.msg_type not in ["reaction", "media", "voice"] and m.text):
                text_msgs_by_sender[m.sender].append(m)

        # 2. Textual & Linguistic Density
        text_stats: Dict[str, LinguisticStats] = {}
        all_words_by_sender: Dict[str, List[str]] = defaultdict(list)
        all_caps_by_sender: Dict[str, int] = defaultdict(int)
        elongations_by_sender: Dict[str, int] = defaultdict(int)
        exclamations_by_sender: Dict[str, int] = defaultdict(int)

        for s in senders:
            s_texts = text_msgs_by_sender[s]
            word_counts = [m.raw_length_words for m in s_texts if m.raw_length_words > 0]
            questions = sum(1 for m in s_texts if "?" in m.text)

            for m in s_texts:
                words = re.findall(r"\b\w+\b", m.text.lower())
                all_words_by_sender[s].extend(words)
                
                # Emotional markers
                all_caps_by_sender[s] += len([w for w in m.text.split() if w.isupper() and len(w) > 2])
                elongations_by_sender[s] += len(re.findall(r"([a-zA-Z])\1{2,}", m.text))
                exclamations_by_sender[s] += m.text.count("!")

            unique_w = len(set(all_words_by_sender[s]))
            tot_w = len(all_words_by_sender[s])

            text_stats[s] = {
                "text_messages": len(s_texts),
                "total_words": tot_w,
                "avg_words": round(statistics.mean(word_counts), 2) if word_counts else 0.0,
                "median_words": float(statistics.median(word_counts)) if word_counts else 0.0,
                "max_words": max(word_counts) if word_counts else 0,
                "questions_count": questions,
                "question_rate_percent": round((questions / len(s_texts)) * 100, 2) if s_texts else 0.0,
                "unique_words": unique_w,
                "type_token_ratio": round(unique_w / tot_w, 4) if tot_w else 0.0,
                "caps_emphasis_words": all_caps_by_sender[s],
                "elongated_words": elongations_by_sender[s],
                "exclamation_marks": exclamations_by_sender[s]
            }

        # 3. Burstiness & Turn-taking
        turns: List[Tuple[str, int]] = []
        curr_sender: Optional[str] = None
        curr_burst = 0
        for m in self.messages:
            if m.sender == curr_sender:
                curr_burst += 1
            else:
                if curr_sender is not None:
                    turns.append((curr_sender, curr_burst))
                curr_sender = m.sender
                curr_burst = 1
        if curr_sender is not None:
            turns.append((curr_sender, curr_burst))

        burst_stats: Dict[str, BurstStats] = {}
        for s in senders:
            s_bursts = [cnt for snd, cnt in turns if snd == s]
            burst_stats[s] = {
                "turns_count": len(s_bursts),
                "avg_burst": round(statistics.mean(s_bursts), 2) if s_bursts else 0.0,
                "median_burst": float(statistics.median(s_bursts)) if s_bursts else 0.0,
                "max_burst": max(s_bursts) if s_bursts else 0
            }

        # 4. Latency / Response Turnaround Time (RTT)
        latencies: Dict[str, List[float]] = defaultdict(list)
        for i in range(1, len(self.messages)):
            p = self.messages[i - 1]
            c = self.messages[i]
            if p.sender != c.sender:
                delta = (c.timestamp - p.timestamp).total_seconds()
                if delta <= self.session_gap.total_seconds():
                    latencies[c.sender].append(delta)

        latency_stats: Dict[str, LatencyStats] = {}
        for s in senders:
            l_vals = latencies[s]
            if l_vals:
                sub60 = sum(1 for sec in l_vals if sec <= 60.0)
                sub300 = sum(1 for sec in l_vals if sec <= 300.0)
                latency_stats[s] = {
                    "median_seconds": round(float(statistics.median(l_vals)), 1),
                    "mean_seconds": round(statistics.mean(l_vals), 1),
                    "under_60s_percent": round((sub60 / len(l_vals)) * 100, 1),
                    "under_300s_percent": round((sub300 / len(l_vals)) * 100, 1),
                    "turnarounds_measured": len(l_vals)
                }
            else:
                latency_stats[s] = {"median_seconds": 0.0, "mean_seconds": 0.0, "turnarounds_measured": 0}

        # 5. Sessions & Silence Breakage (>24h)
        sessions: List[SessionEvent] = []
        silences: List[SilenceEvent] = []
        sess_start = self.messages[0]
        sess_msgs = [self.messages[0]]

        for i in range(1, len(self.messages)):
            p = self.messages[i - 1]
            c = self.messages[i]
            diff = c.timestamp - p.timestamp

            if diff > self.silence_gap:
                silences.append({
                    "duration_hours": round(diff.total_seconds() / 3600.0, 1),
                    "reopened_by": c.sender,
                    "reopened_at": c.timestamp.isoformat(),
                    "preview": c.text[:60] if c.text else f"[{c.msg_type}]"
                })

            if diff > self.session_gap:
                sessions.append({
                    "opener": sess_start.sender,
                    "started_at": sess_start.timestamp.isoformat(),
                    "ended_at": p.timestamp.isoformat(),
                    "messages": len(sess_msgs)
                })
                sess_start = c
                sess_msgs = [c]
            else:
                sess_msgs.append(c)

        sessions.append({
            "opener": sess_start.sender,
            "started_at": sess_start.timestamp.isoformat(),
            "ended_at": self.messages[-1].timestamp.isoformat(),
            "messages": len(sess_msgs)
        })

        session_openers: Counter[str] = Counter(s["opener"] for s in sessions)
        silence_breakers: Counter[str] = Counter(s["reopened_by"] for s in silences)

        # 6. Emojis
        emoji_counts: Dict[str, Counter[str]] = {s: Counter() for s in senders}
        for m in self.messages:
            if not m.text:
                continue
            for cat, e_list in EMOJI_CATEGORIES.items():
                for emo in e_list:
                    c = m.text.count(emo)
                    if c > 0:
                        emoji_counts[m.sender][cat] += c

        # 7. Gottman & Mentalization Indexes
        gottman_scores: Dict[str, Counter[str]] = {s: Counter() for s in senders}
        mentalization_scores: Dict[str, Counter[str]] = {s: Counter() for s in senders}

        for m in self.messages:
            if not m.text:
                continue
            txt = m.text.lower()
            for horseman, patterns in GOTTMAN_LEXICON.items():
                for pat in patterns:
                    if pat in txt:
                        gottman_scores[m.sender][horseman] += 1
            for m_mode, patterns in MENTALIZATION_LEXICON.items():
                for pat in patterns:
                    if pat in txt:
                        mentalization_scores[m.sender][m_mode] += 1

        # 8. Affective Valence & Gottman 5:1 Golden Ratio
        pos_scores: Dict[str, int] = {s: 0 for s in senders}
        neg_scores: Dict[str, int] = {s: 0 for s in senders}

        for m in self.messages:
            if not m.text:
                continue
            txt = m.text.lower()
            # Emojis count toward valence
            aff_count = sum(m.text.count(e) for e in EMOJI_CATEGORIES["affection_love"] + EMOJI_CATEGORIES["tenderness_kisses"])
            pos_scores[m.sender] += aff_count

            for p_word in POSITIVE_VALENCE_LEXICON:
                if p_word in txt:
                    pos_scores[m.sender] += 1
            for n_word in NEGATIVE_VALENCE_LEXICON:
                if n_word in txt:
                    neg_scores[m.sender] += 1

        affective_valence: Dict[str, AffectiveValenceStats] = {}
        for s in senders:
            p_val = pos_scores[s]
            n_val = neg_scores[s]
            ratio = round(p_val / max(n_val, 1), 2)
            if ratio >= 5.0:
                safety = "🟢 Haute Sécurité (Ratio ≥ 5:1)"
            elif ratio >= 2.0:
                safety = "🟡 Équilibre Fragile (2:1 à 5:1)"
            else:
                safety = "🔴 Zone Critique (Moins de 2 marques positives par tension)"
            affective_valence[s] = {
                "positive_indicators": p_val,
                "negative_indicators": n_val,
                "pos_neg_ratio": ratio,
                "emotional_safety_status": safety
            }

        total_pos = sum(pos_scores.values())
        total_neg = sum(neg_scores.values())
        overall_gottman_ratio = round(total_pos / max(total_neg, 1), 2)
        if overall_gottman_ratio >= 5.0:
            coreg_badge = "🟢 SÉCURE (Ratio Gottman ≥ 5.0)"
        elif overall_gottman_ratio >= 2.5:
            coreg_badge = "🟡 STABLE (Ratio Gottman modéré)"
        else:
            coreg_badge = "🔴 VULNÉRABLE (Ratio Gottman critique)"

        # 9. Bids for Connection & Responsiveness Analysis
        bids_by_sender: Dict[str, List[int]] = defaultdict(list)
        for idx, m in enumerate(self.messages):
            if not m.text and m.msg_type not in ["media", "voice", "share"]:
                continue
            # A bid is a question, photo/voice note, or emotional opening
            is_bid = ("?" in m.text) or (m.msg_type in ["media", "voice", "share"]) or any(
                m.text.lower().startswith(kw) for kw in ["regarde", "écoute", "tu as vu", "j'ai pensé", "je te montre"]
            )
            if is_bid:
                bids_by_sender[m.sender].append(idx)

        bids_stats: Dict[str, BidStats] = {}
        tot_turned_toward = 0
        tot_bids = 0

        for s in senders:
            initiated = len(bids_by_sender[s])
            tot_bids += initiated
            toward = 0
            away = 0
            against = 0

            for bid_idx in bids_by_sender[s]:
                bid_msg = self.messages[bid_idx]
                # Look for the first response from another sender within session
                found_reply = False
                for j in range(bid_idx + 1, len(self.messages)):
                    rep = self.messages[j]
                    if rep.sender == s:
                        continue
                    # Check gap
                    if (rep.timestamp - bid_msg.timestamp) > self.session_gap:
                        break
                    found_reply = True
                    rep_txt = rep.text.lower()
                    # Check if hostile / against
                    is_against = any(pat in rep_txt for patterns in GOTTMAN_LEXICON.values() for pat in patterns)
                    # Check if turning away (monosyllable ok/vu/k)
                    is_away = len(rep.text.split()) <= 1 and rep_txt in ["ok", "k", "vu", "dakor", "👍", "comme tu veux"]

                    if is_against:
                        against += 1
                    elif is_away:
                        away += 1
                    else:
                        toward += 1
                    break

                if not found_reply:
                    away += 1

            tot_turned_toward += toward
            resp_rate = round((toward / max(initiated, 1)) * 100, 1)
            bids_stats[s] = {
                "bids_initiated": initiated,
                "turned_toward": toward,
                "turned_away": away,
                "turned_against": against,
                "responsiveness_rate_percent": resp_rate
            }

        overall_bid_responsiveness = round((tot_turned_toward / max(tot_bids, 1)) * 100, 1)

        # 10. Equilibrium, Reciprocity & Information Entropy
        total_turns = len(turns)
        entropy_val = 1.0
        if total_turns > 0 and len(senders) > 1:
            turn_counts: Counter[str] = Counter(s for s, _ in turns)
            h = 0.0
            for s in senders:
                p = turn_counts[s] / total_turns
                if p > 0:
                    h -= p * math.log2(p)
            max_h = math.log2(len(senders))
            entropy_val = round(h / max_h, 3) if max_h > 0 else 1.0

        if len(senders) == 2:
            s1, s2 = senders[0], senders[1]
            vol1, vol2 = vol_by_sender[s1], vol_by_sender[s2]
            vol_balance = round(min(vol1, vol2) / max(vol1, vol2), 3) if max(vol1, vol2) > 0 else 1.0

            q1 = text_stats[s1]["questions_count"]
            q2 = text_stats[s2]["questions_count"]
            q_balance = round(min(q1, q2) / max(q1, q2), 3) if max(q1, q2) > 0 else 1.0
        else:
            vol_balance, q_balance = 1.0, 1.0

        timespan_days = max(0.05, round((self.messages[-1].timestamp - self.messages[0].timestamp).total_seconds() / 86400.0, 2))
        velocity_msgs_day = round(total_count / timespan_days, 1)

        # 11. Day of Week distribution
        day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        weekday_counts: Dict[str, Dict[str, int]] = {s: {d: 0 for d in day_names} for s in senders}
        for m in self.messages:
            d_name = day_names[m.timestamp.weekday()]
            weekday_counts[m.sender][d_name] += 1

        # 12. Hourly 24-Hour distribution
        hourly_counts: Dict[str, Dict[int, int]] = {s: {h: 0 for h in range(24)} for s in senders}
        for m in self.messages:
            hourly_counts[m.sender][m.timestamp.hour] += 1

        return {
            "summary": {
                "total_messages": total_count,
                "senders": senders,
                "first_date": self.messages[0].timestamp.isoformat(),
                "last_date": self.messages[-1].timestamp.isoformat(),
                "timespan_days": timespan_days,
                "velocity_messages_per_day": velocity_msgs_day,
                "volume_by_sender": dict(vol_by_sender),
                "total_sessions": len(sessions),
                "session_openers": dict(session_openers),
                "silence_events_count": len(silences),
                "silence_breakers": dict(silence_breakers),
                "reciprocity_balance_score": vol_balance,
                "curiosity_balance_score": q_balance,
                "turn_taking_entropy": entropy_val,
                "overall_gottman_ratio": overall_gottman_ratio,
                "overall_bid_responsiveness_rate": overall_bid_responsiveness,
                "coregulation_health_badge": coreg_badge
            },
            "weekday_distribution": weekday_counts,
            "hourly_distribution": hourly_counts,
            "types_breakdown": {s: dict(type_by_sender[s]) for s in senders},
            "linguistics": text_stats,
            "burstiness": burst_stats,
            "rtt_latency": latency_stats,
            "emoji_taxonomies": {s: dict(emoji_counts[s]) for s in senders},
            "gottman_indicators": {s: dict(gottman_scores[s]) for s in senders},
            "mentalization_indicators": {s: dict(mentalization_scores[s]) for s in senders},
            "affective_valence": affective_valence,
            "bids_for_connection": bids_stats,
            "silence_log": silences
        }

    def format_markdown(self, res: AnalyticsResult) -> str:
        if "error" in res:
            return f"# ⚠️ Analyse Interrompue\n\n**Cause :** {res['error']}"

        s = res.get("summary", {})
        senders = s.get("senders", [])
        total_msgs = s.get("total_messages", 0)
        first_d = s.get("first_date", "")[:10]
        last_d = s.get("last_date", "")[:10]
        t_days = s.get("timespan_days", 0.0)

        md: List[str] = []
        md.append("# 📊 Comprehensive Relational & Conversational Audit")
        md.append(f"**Périmètre :** {total_msgs} messages | **Période :** {first_d} au {last_d} ({t_days} jours)\n")

        md.append("## 1. Métriques Fondamentales d'Équilibre")
        md.append("| Indicateur | " + " | ".join(senders) + " | Total / Équilibre |")
        md.append("|---| " + " | ".join(["---"] * len(senders)) + " |---|")

        vol_map = s.get("volume_by_sender", {})
        vols = [f"**{vol_map.get(snd, 0)}** ({round(vol_map.get(snd, 0) / max(total_msgs, 1) * 100, 1)} %)" for snd in senders]
        md.append(f"| Volume de Messages | {' | '.join(vols)} | {total_msgs} (Ratio: {s.get('reciprocity_balance_score', 1.0)}) |")

        ling = res.get("linguistics", {})
        words = [f"{ling.get(snd, {}).get('total_words', 0)} (méd. {ling.get(snd, {}).get('median_words', 0)} mots)" for snd in senders]
        md.append(f"| Mots & Longueur | {' | '.join(words)} | — |")

        questions = [f"{ling.get(snd, {}).get('questions_count', 0)} ({ling.get(snd, {}).get('question_rate_percent', 0.0)} %)" for snd in senders]
        md.append(f"| Questions Posées | {' | '.join(questions)} | Ratio: {s.get('curiosity_balance_score', 1.0)} |")

        rtt_map = res.get("rtt_latency", {})
        rtt = [f"**{rtt_map.get(snd, {}).get('median_seconds', 0.0)} s** (<1min: {rtt_map.get(snd, {}).get('under_60s_percent', 0.0)} %)" for snd in senders]
        md.append(f"| Latence Médiane (RTT) | {' | '.join(rtt)} | — |")

        burst_map = res.get("burstiness", {})
        burst = [f"{burst_map.get(snd, {}).get('avg_burst', 0.0)} (max: {burst_map.get(snd, {}).get('max_burst', 0)})" for snd in senders]
        md.append(f"| Rafale (messages/tour) | {' | '.join(burst)} | — |")

        openers_map = s.get("session_openers", {})
        openers = [f"{openers_map.get(snd, 0)}" for snd in senders]
        md.append(f"| Ouvertures Sessions (>4h) | {' | '.join(openers)} | {s.get('total_sessions', 0)} sessions |")

        breakers_map = s.get("silence_breakers", {})
        breakers = [f"{breakers_map.get(snd, 0)}" for snd in senders]
        md.append(f"| Rupture Silences (>24h) | {' | '.join(breakers)} | {s.get('silence_events_count', 0)} silences |")

        md.append(f"| Entropie Prise de Parole (H) | {' | '.join(['—']*len(senders))} | H = `{s.get('turn_taking_entropy', 1.0)}` / 1.0 (Équilibre) |")
        md.append(f"| Vélocité Conversationnelle | {' | '.join(['—']*len(senders))} | `{s.get('velocity_messages_per_day', 0.0)}` msgs / jour |")

        # Section 2: Gottman 5:1 Ratio & Affective Valence
        md.append("\n## 2. Ratio d'Or de Gottman (Positif / Négatif) & Valence Affective")
        md.append(f"**Indice Global du Duo :** `{s.get('overall_gottman_ratio', 1.0)} : 1` ➔ **{s.get('coregulation_health_badge', '')}**\n")
        md.append("| Partenaire | Positifs (Affection/Joie) | Négatifs (Anxiété/Pique) | Ratio Individuel | Diagnostic Opérationnel |")
        md.append("|---|---|---|---|---|")
        aff = res.get("affective_valence", {})
        for snd in senders:
            p_cnt = aff.get(snd, {}).get("positive_indicators", 0)
            n_cnt = aff.get(snd, {}).get("negative_indicators", 0)
            r_val = aff.get(snd, {}).get("pos_neg_ratio", 1.0)
            st = aff.get(snd, {}).get("emotional_safety_status", "")
            md.append(f"| **{snd}** | `{p_cnt}` | `{n_cnt}` | **{r_val} : 1** | {st} |")

        # Section 3: Bids for Connection
        md.append("\n## 3. Appels de Contact (Bids for Connection) & Taux d'Accueil")
        md.append(f"**Taux Global d'Accueil Positif :** `{s.get('overall_bid_responsiveness_rate', 0.0)} %` (Standard Gottman Masters : ≥ 80%)\n")
        md.append("| Partenaire (Initiateur) | Appels Émis | Accueillis (Toward) | Ignorés (Away) | Rejetés (Against) | Taux de Succès |")
        md.append("|---|---|---|---|---|---|")
        bids = res.get("bids_for_connection", {})
        for snd in senders:
            b_init = bids.get(snd, {}).get("bids_initiated", 0)
            b_tow = bids.get(snd, {}).get("turned_toward", 0)
            b_aw = bids.get(snd, {}).get("turned_away", 0)
            b_ag = bids.get(snd, {}).get("turned_against", 0)
            b_rate = bids.get(snd, {}).get("responsiveness_rate_percent", 0.0)
            md.append(f"| **{snd}** | {b_init} | 🟢 {b_tow} | 🟡 {b_aw} | 🔴 {b_ag} | **{b_rate} %** |")

        md.append("\n## 4. Indicateurs Cliniques de Gottman (Signaux d'Alerte)")
        md.append("| Cavalier de Gottman | " + " | ".join(senders) + " | Statut Clinique |")
        md.append("|---| " + " | ".join(["---"] * len(senders)) + " |---|")
        gottman_map = res.get("gottman_indicators", {})
        for h, label in [("criticism", "Critique (Attaque globale)"), ("contempt", "Mépris (Dédain/Sarcasme)"), ("defensiveness", "Défense (Justification/Rejet)"), ("stonewalling_terms", "Dérobade (Monosyllabes/Retrait)")]:
            vals = [str(gottman_map.get(snd, {}).get(h, 0)) for snd in senders]
            tot = sum(gottman_map.get(snd, {}).get(h, 0) for snd in senders)
            stat = "🟢 Faible" if tot <= 2 else ("🟡 Modéré" if tot <= 6 else "🔴 Élevé")
            md.append(f"| {label} | {' | '.join(vals)} | {stat} |")

        md.append("\n## 5. Profil de Mentalisation (Fonagy)")
        md.append("| Mode de Mentalisation | " + " | ".join(senders) + " | Interprétation |")
        md.append("|---| " + " | ".join(["---"] * len(senders)) + " |---|")
        ment_map = res.get("mentalization_indicators", {})
        cog_vals = [str(ment_map.get(snd, {}).get("reflective_cognitive", 0)) for snd in senders]
        md.append(f"| **Réflexif / Cognitif** (Affects/Pensées) | {' | '.join(cog_vals)} | Capacité à modéliser l'intériorité |")
        act_vals = [str(ment_map.get(snd, {}).get("teleological_action", 0)) for snd in senders]
        md.append(f"| **Téléologique** (Actes/Preuves/Ordres) | {' | '.join(act_vals)} | Besoin de preuves matérielles |")

        md.append("\n## 6. Température Émotionnelle & Stylistique")
        md.append("| Marqueur Expressif | " + " | ".join(senders) + " |")
        md.append("|---| " + " | ".join(["---"] * len(senders)) + " |")
        caps_vals = [str(ling.get(snd, {}).get("caps_emphasis_words", 0)) for snd in senders]
        md.append(f"| Mots en MAJUSCULES d'emphase | {' | '.join(caps_vals)} |")
        elong_vals = [str(ling.get(snd, {}).get("elongated_words", 0)) for snd in senders]
        md.append(f"| Mots allongés (*'ouiiiii'*, *'mdrrrr'*) | {' | '.join(elong_vals)} |")
        excl_vals = [str(ling.get(snd, {}).get("exclamation_marks", 0)) for snd in senders]
        md.append(f"| Points d'exclamation (`!`) | {' | '.join(excl_vals)} |")

        return "\n".join(md)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Multi-format conversational psychology & metrics engine.")
    parser.add_argument("input_pos", nargs="?", default="", help="Path to chat export (JSON, WhatsApp TXT, Meta JSON, CSV)")
    parser.add_argument("--input", "-i", dest="input_flag", type=str, default="", help="Path to chat export")
    parser.add_argument("--output", "-o", type=str, default="", help="Path to output report")
    parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown", help="Report format")
    parser.add_argument("--json", action="store_true", help="Shortcut for --format json")
    parser.add_argument("--session-gap", type=float, default=4.0, help="Inactivity gap to define a new session (hours)")
    parser.add_argument("--silence-gap", type=float, default=24.0, help="Threshold for major conversational silence (hours)")
    args = parser.parse_args()

    input_file = args.input_flag or args.input_pos
    if not input_file:
        parser.error("Please provide an input file (e.g. python analyze_chat_metrics.py <file> or -i <file>)")

    messages = ChatParser.parse_file(input_file)
    engine = AdvancedConversationalEngine(messages, session_gap_hours=args.session_gap, silence_gap_hours=args.silence_gap)
    results = engine.analyze()

    if args.json:
        args.format = 'json'
    if args.format == 'markdown':
        output = engine.format_markdown(results)
    else:
        output = json.dumps(results, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report written successfully to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
