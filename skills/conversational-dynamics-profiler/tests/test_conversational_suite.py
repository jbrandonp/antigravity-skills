#!/usr/bin/env python3
"""
test_conversational_suite.py
----------------------------
Comprehensive automated regression & edge-case test suite for conversational-dynamics-profiler.
Validates:
- Multi-format ingestion (Meta JSON with latin1 repairs, WhatsApp TXT, Generic JSON, CSV)
- RTT Latency, Burstiness, and Turn-Taking Shannon Entropy
- Gottman Indicators and Mentalization Lexicon detection
- Clinical Health Score generation & Markdown report output
- 24-Hour circadian hourly distribution and standalone HTML dashboard export
- Multi-locale WhatsApp date parsing (EU, US 12h AM/PM, 2-digit year)
- Resilient empty and malformed input handling (zero uncaught exceptions)
- End-to-end interactive CLI batch pipeline producing all 4 artifacts
"""

import datetime
import json
import os
import sys
import tempfile
import unittest

# Add scripts directory to path
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from analyze_chat_metrics import ChatParser, AdvancedConversationalEngine, Message
from generate_relationship_report import RelationshipReportSynthesizer
from export_html_dashboard import generate_html_dashboard
from simulate_conversational_scenarios import run_simulation, format_markdown_simulation
from universal_chat_converter import UniversalConverter


class TestConversationalDynamicsSuite(unittest.TestCase):

    def test_meta_json_parser_with_encoding_fix(self):
        """Validates parsing Meta JSON export and fixing latin-1 mangled UTF-8 text."""
        mangled_sender = "Tatiana Garcia"
        mangled_text = "Je t\u00c3\u00a9l\u00c3\u00a9phone demain mon coeur !"
        raw_meta = {
            "messages": [
                {
                    "sender_name": mangled_sender,
                    "timestamp_ms": 1762128000000,
                    "content": mangled_text
                },
                {
                    "sender_name": "Brandon",
                    "timestamp_ms": 1762128030000,
                    "content": "Super, je t'aime ❤️"
                }
            ]
        }
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8") as f:
            json.dump(raw_meta, f)
            tmp_path = f.name

        try:
            msgs = ChatParser.parse_file(tmp_path)
            self.assertEqual(len(msgs), 2)
            self.assertEqual(msgs[0].sender, "Tatiana Garcia")
            self.assertIn("téléphone", msgs[0].text)
        finally:
            os.remove(tmp_path)

    def test_whatsapp_text_parser_multiline(self):
        """Validates parsing WhatsApp text export including multiline continuation."""
        wa_text = """[05/11/2026, 15:30:00] Alice: Coucou ! Tu vas bien ?
J'ai acheté les sauces piquantes.
[05/11/2026, 15:30:45] Bob: Trop bien !
Merci chaton 🥰
"""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write(wa_text)
            tmp_path = f.name

        try:
            msgs = ChatParser.parse_file(tmp_path)
            self.assertEqual(len(msgs), 2)
            self.assertEqual(msgs[0].sender, "Alice")
            self.assertIn("sauces piquantes", msgs[0].text)
            self.assertEqual(msgs[1].sender, "Bob")
            self.assertIn("Merci chaton", msgs[1].text)
        finally:
            os.remove(tmp_path)

    def test_shannon_entropy_and_rtt(self):
        """Validates Shannon entropy of turn-taking and response turnaround time."""
        dt_base = datetime.datetime(2026, 11, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        messages = [
            Message("A", dt_base, "Salut"),
            Message("B", dt_base + datetime.timedelta(seconds=20), "Coucou"),
            Message("A", dt_base + datetime.timedelta(seconds=40), "Ca va ?"),
            Message("B", dt_base + datetime.timedelta(seconds=60), "Super et toi ?"),
        ]
        engine = AdvancedConversationalEngine(messages)
        res = engine.analyze()
        summary = res["summary"]

        self.assertAlmostEqual(summary["turn_taking_entropy"], 1.0, places=2)
        self.assertEqual(summary["total_messages"], 4)
        self.assertIn("A", summary["senders"])
        self.assertIn("B", summary["senders"])
        self.assertEqual(res["rtt_latency"]["B"]["median_seconds"], 20.0)

    def test_gottman_and_mentalization_detection(self):
        """Validates detection of Gottman warning signs and Fonagy mentalization modes."""
        dt_base = datetime.datetime(2026, 11, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        messages = [
            Message("A", dt_base, "Tu es toujours à deux vitesses, tu ne penses jamais à moi"),
            Message("B", dt_base + datetime.timedelta(seconds=15), "Désolé, je comprends ce que tu ressens et ton intention, je t'aime"),
        ]
        engine = AdvancedConversationalEngine(messages)
        res = engine.analyze()

        self.assertGreaterEqual(res["gottman_indicators"]["A"]["criticism"], 1)
        self.assertGreaterEqual(res["mentalization_indicators"]["B"]["reflective_cognitive"], 1)

    def test_relationship_report_synthesizer(self):
        """Validates report generation and health score computation."""
        dt_base = datetime.datetime(2026, 11, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        messages = [
            Message("Alice", dt_base, "Je t'aime mon cœur 🥰"),
            Message("Bob", dt_base + datetime.timedelta(seconds=30), "Moi aussi je t'aime ❤️"),
        ]
        engine = AdvancedConversationalEngine(messages)
        analytics = engine.analyze()
        synth = RelationshipReportSynthesizer(analytics)
        report = synth.generate_markdown()

        self.assertIn("# 📑 Rapport d'Intelligence Relationnelle", report)
        self.assertIn("Score Obtenu", report)
        self.assertIn("Sécurité Gottman", report)

    def test_export_html_dashboard(self):
        """Validates standalone HTML/SVG dashboard generator."""
        dt_base = datetime.datetime(2026, 11, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        messages = [
            Message("Alice", dt_base, "Salut !"),
            Message("Bob", dt_base + datetime.timedelta(seconds=25), "Coucou chou ❤️"),
        ]
        engine = AdvancedConversationalEngine(messages)
        analytics = engine.analyze()

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html", encoding="utf-8") as f:
            tmp_html = f.name
        f.close()

        try:
            content = generate_html_dashboard(analytics, tmp_html)
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("Conversational Dynamics & Intelligence Dashboard", content)
            self.assertTrue(os.path.exists(tmp_html))
            self.assertGreater(os.path.getsize(tmp_html), 500)
        finally:
            if os.path.exists(tmp_html):
                os.remove(tmp_html)

    def test_simulate_conversational_scenarios(self):
        """Validates conversational crisis stress testing simulator."""
        sims = run_simulation()
        self.assertIn("unannounced_silence", sims)
        self.assertIn("construction_stress", sims)
        md = format_markdown_simulation(sims)
        self.assertIn("# 🔮 Simulateur Prédictif", md)
        self.assertIn("Scénario 1", md)

    def test_universal_converter_with_anonymization(self):
        """Validates UniversalConverter with PII redaction (email, phone, IBAN)."""
        raw_wa = """[05/11/2026, 12:00:00] Alice: Mon email est alice@example.com et mon IBAN BE68539007547034.
[05/11/2026, 12:00:30] Bob: Reçu ! Mon num est 0471234567.
"""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write(raw_wa)
            tmp_in = f.name

        try:
            res = UniversalConverter.convert_file(tmp_in, anonymize=True)
            self.assertEqual(len(res), 2)
            self.assertIn("[EMAIL_REDACTED]", res[0]["text"])
            self.assertIn("[IBAN_REDACTED]", res[0]["text"])
            self.assertIn("[PHONE_BE_REDACTED]", res[1]["text"])
            self.assertNotIn("alice@example.com", res[0]["text"])
        finally:
            os.remove(tmp_in)

    def test_interactive_profiler_cli_batch_pipeline(self):
        """Validates end-to-end batch pipeline execution producing all 4 artifacts."""
        import subprocess
        raw_wa = """[05/11/2026, 12:00:00] Alice: Salut chou ! Tu as faim ? ❤️
[05/11/2026, 12:00:30] Bob: Oui trop ! On mange des pâtes ? 🥰
"""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write(raw_wa)
            tmp_in = f.name

        tmp_out_prefix = os.path.join(tempfile.gettempdir(), "test_pipeline_run_v7")

        cli_script = os.path.join(SCRIPTS_DIR, "interactive_profiler_cli.py")
        cmd = [sys.executable, "-B", cli_script, "--run-all", "-i", tmp_in, "-o", tmp_out_prefix, "--anonymize"]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.assertEqual(res.returncode, 0)
            self.assertTrue(os.path.exists(f"{tmp_out_prefix}_normalized.json"))
            self.assertTrue(os.path.exists(f"{tmp_out_prefix}_metrics.md"))
            self.assertTrue(os.path.exists(f"{tmp_out_prefix}_rapport_sante.md"))
            self.assertTrue(os.path.exists(f"{tmp_out_prefix}_dashboard.html"))
        finally:
            for ext in [".txt", "_normalized.json", "_metrics.md", "_rapport_sante.md", "_dashboard.html"]:
                p = f"{tmp_out_prefix}{ext}"
                if os.path.exists(p):
                    os.remove(p)
            if os.path.exists(tmp_in):
                os.remove(tmp_in)

    def test_hourly_circadian_distribution_and_chart(self):
        """Validates that hourly distribution is populated for 24h and passed to HTML dashboard."""
        dt_14h = datetime.datetime(2026, 11, 1, 14, 15, 0, tzinfo=datetime.timezone.utc)
        dt_21h = datetime.datetime(2026, 11, 1, 21, 45, 0, tzinfo=datetime.timezone.utc)
        messages = [
            Message("Alice", dt_14h, "Message de 14h"),
            Message("Bob", dt_21h, "Message de 21h"),
        ]
        engine = AdvancedConversationalEngine(messages)
        res = engine.analyze()

        self.assertIn("hourly_distribution", res)
        self.assertEqual(res["hourly_distribution"]["Alice"][14], 1)
        self.assertEqual(res["hourly_distribution"]["Bob"][21], 1)
        self.assertEqual(res["hourly_distribution"]["Alice"][0], 0)

        html = generate_html_dashboard(res)
        self.assertIn("14h", html)
        self.assertIn("21h", html)
        self.assertIn('fill="#38bdf8"', html)

    def test_resilient_empty_corpus_handling(self):
        """Validates that empty files and corpuses are handled safely without unhandled exceptions."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write("")
            empty_path = f.name

        try:
            # 1. Universal converter returns [] on empty file
            conv_res = UniversalConverter.convert_file(empty_path)
            self.assertEqual(conv_res, [])

            # 2. ChatParser returns [] on empty file
            parsed_msgs = ChatParser.parse_file(empty_path)
            self.assertEqual(parsed_msgs, [])

            # 3. Engine returns clean error dict
            engine = AdvancedConversationalEngine(parsed_msgs)
            analytics = engine.analyze()
            self.assertIn("error", analytics)

            # 4. format_markdown handles error dict safely
            md = engine.format_markdown(analytics)
            self.assertIn("⚠️ Analyse Interrompue", md)

            # 5. Report synthesizer handles error dict safely
            synth = RelationshipReportSynthesizer(analytics)
            rep = synth.generate_markdown()
            self.assertIn("⚠️ Rapport Non Généré", rep)

            # 6. HTML dashboard generator handles error dict safely
            html = generate_html_dashboard(analytics)
            self.assertIn("⚠️ Corpus Inexploitable", html)
        finally:
            if os.path.exists(empty_path):
                os.remove(empty_path)

    def test_whatsapp_multilocale_date_formats(self):
        """Validates WhatsApp parsing with US format (12h AM/PM) and 2-digit years."""
        wa_us = """11/5/26, 2:30 PM - Alice: Hey there!
11/5/26, 2:35 PM - Bob: Hi! How are you?
"""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write(wa_us)
            tmp_us = f.name

        try:
            msgs = ChatParser.parse_file(tmp_us)
            self.assertEqual(len(msgs), 2)
            self.assertEqual(msgs[0].sender, "Alice")
            self.assertEqual(msgs[0].timestamp.hour, 14)
            self.assertEqual(msgs[0].timestamp.minute, 30)
            self.assertEqual(msgs[1].sender, "Bob")
            self.assertEqual(msgs[1].timestamp.hour, 14)
            self.assertEqual(msgs[1].timestamp.minute, 35)
        finally:
            os.remove(tmp_us)

    def test_comprehensive_guides_and_references_presence(self):
        """Validates that psychological, behavioral, and long-term guides exist and contain key models."""
        ref_dir = os.path.join(os.path.dirname(SCRIPTS_DIR), "references")
        tmpl_dir = os.path.join(os.path.dirname(SCRIPTS_DIR), "templates")

        # 1. Psychological & Clinical Profiling Guide
        psych_path = os.path.join(ref_dir, "psychological_and_clinical_profiling_guide.md")
        self.assertTrue(os.path.exists(psych_path))
        with open(psych_path, "r", encoding="utf-8") as f:
            psych_content = f.read()
        self.assertIn("Kernberg", psych_content)
        self.assertIn("Vaillant", psych_content)
        self.assertIn("RSD", psych_content)

        # 2. Behavioral Analysis & Conditioning Guide
        behav_path = os.path.join(ref_dir, "behavioral_analysis_and_conditioning_guide.md")
        self.assertTrue(os.path.exists(behav_path))
        with open(behav_path, "r", encoding="utf-8") as f:
            behav_content = f.read()
        self.assertIn("ANTÉCÉDENT", behav_content)
        self.assertIn("Skinner", behav_content)
        self.assertIn("Extinction", behav_content)

        # 3. Long-Term Relationship Guide & Strategy
        lt_path = os.path.join(ref_dir, "long_term_relationship_guide_and_strategy.md")
        self.assertTrue(os.path.exists(lt_path))
        with open(lt_path, "r", encoding="utf-8") as f:
            lt_content = f.read()
        self.assertIn("Sound Relationship House", lt_content)
        self.assertIn("Esther Perel", lt_content)
        self.assertIn("69 %", lt_content)

        # 4. Nonviolent Communication & Co-regulation guides
        cnv_path = os.path.join(ref_dir, "nonviolent_communication_and_reframing.md")
        self.assertTrue(os.path.exists(cnv_path))
        with open(cnv_path, "r", encoding="utf-8") as f:
            cnv_content = f.read()
        self.assertIn("OSBD", cnv_content)
        self.assertIn("Marshall Rosenberg", cnv_content)

        coreg_path = os.path.join(ref_dir, "coregulation_and_attachment_repair.md")
        self.assertTrue(os.path.exists(coreg_path))
        with open(coreg_path, "r", encoding="utf-8") as f:
            coreg_content = f.read()
        self.assertIn("Couple Bubble", coreg_content)
        self.assertIn("Sue Johnson", coreg_content)

        # 5. Template integration
        audit_tmpl = os.path.join(tmpl_dir, "relational_audit_template.md")
        self.assertTrue(os.path.exists(audit_tmpl))
        with open(audit_tmpl, "r", encoding="utf-8") as f:
            tmpl_content = f.read()
        self.assertIn("psychological_and_clinical_profiling_guide.md", tmpl_content)
        self.assertIn("behavioral_analysis_and_conditioning_guide.md", tmpl_content)
        self.assertIn("long_term_relationship_guide_and_strategy.md", tmpl_content)

    def test_gottman_golden_ratio_and_bids_calculation(self):
        """Validates Gottman 5:1 golden ratio and bids for connection responsiveness."""
        dt_base = datetime.datetime(2026, 11, 1, 10, 0, 0, tzinfo=datetime.timezone.utc)
        messages = [
            Message("Alice", dt_base, "Tu as faim mon coeur ? 🥰"), # Bid (question + positive)
            Message("Bob", dt_base + datetime.timedelta(seconds=20), "Oui trop, je t'aime ❤️"), # Turned toward + positive
            Message("Alice", dt_base + datetime.timedelta(seconds=40), "Regarde cette photo de notre futur salon"), # Bid
            Message("Bob", dt_base + datetime.timedelta(seconds=60), "C'est magnifique ! Tu as trop bon goût"), # Turned toward + positive
        ]
        engine = AdvancedConversationalEngine(messages)
        res = engine.analyze()

        summary = res["summary"]
        self.assertIn("overall_gottman_ratio", summary)
        self.assertIn("overall_bid_responsiveness_rate", summary)
        self.assertGreaterEqual(summary["overall_gottman_ratio"], 5.0)
        self.assertEqual(summary["overall_bid_responsiveness_rate"], 100.0)

        # Check bids dict
        bids = res["bids_for_connection"]
        self.assertEqual(bids["Alice"]["bids_initiated"], 2)
        self.assertEqual(bids["Alice"]["turned_toward"], 2)
        self.assertEqual(bids["Alice"]["turned_away"], 0)

    def test_markov_state_machine_and_cnv_reframe(self):
        """Validates Markov dyadic state machine and Non-Violent Communication reframer."""
        from simulate_conversational_scenarios import compute_markov_state_machine, cnv_reframe_message

        transitions = compute_markov_state_machine(gottman_ratio=6.0, stonewalling_count=0)
        self.assertEqual(len(transitions), 3)
        self.assertIn("Ventral Vagal", transitions[0]["from_state"])
        self.assertIn("Sympathique", transitions[0]["to_state"])

        cnv_res = cnv_reframe_message("Tu es toujours en retard, tu ne penses jamais à moi !")
        self.assertIn("original_message", cnv_res)
        self.assertIn("observation", cnv_res)
        self.assertIn("sentiment", cnv_res)
        self.assertIn("besoin", cnv_res)
        self.assertIn("demande", cnv_res)
        self.assertIn("suggested_reformulation", cnv_res)
        self.assertIn("« Quand", cnv_res["suggested_reformulation"])


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    unittest.main()
