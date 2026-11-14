#!/usr/bin/env python3
"""
test_harness.py - End-to-end test suite for brivael-twitter-system tools.
Audits the consolidated 4-pillar architecture:
Pillar 0: Master Engine
Pillar 1: Systemic Investigation
Pillar 2: French Cultural Offensive
Pillar 3: Minimalist Sniper
"""

import subprocess
import sys


def run_tests() -> None:
    print("=" * 60)
    print("🧪 DÉBUT DU BANC DE TEST : ARCHITECTURE 4 PILIERS CONSOLIDÉS")
    print("=" * 60)

    # Test 1 : Pilier 2 - Offensive Culturelle ("Déroulons" + "Étage sans fenêtre")
    valid_text_offensive = (
        "Yesterday on national TV, three pundits mocked French tech startups.\r\n\r\n"
        "Déroulons.\r\n\r\n"
        "I will tell you where I speak from.\r\n"
        "I come from Brittany.\r\n"
        "I coded my company alone.\r\n"
        "Zero subsidies.\r\n\r\n"
        "Where do you speak from?\r\n"
        "From the windowless floor.\r\n"
        "A heated bubble paid by taxes.\r\n\r\n"
        "Reality is coming.\r\n"
        "And reality never laughs."
    )
    res1 = subprocess.run(
        ["python", "c:/Users/brand/.claude/skills/brivael-twitter-system/scripts/verify_brivael_post.py", valid_text_offensive, "--mode", "offensive"],
        capture_output=True,
        text=True,
    )
    assert res1.returncode == 0, f"Test 1 Failed: {res1.stdout}\n{res1.stderr}"
    print("✅ TEST 1 RÉUSSI : Pilier 2 'offensive' validé (Code 0, Score >= 80).")

    # Test 2 : Pilier 1 - Investigation Systémique ("Step 1..." + "Now connect it")
    valid_text_investigation = (
        "The AI safety narrative is a corporate cartelization play.\r\n\r\n"
        "Step 1: Proprietary labs realize open weights are winning.\r\n"
        "Step 2: They lobby parliaments on rogue algorithms.\r\n"
        "Step 3: They demand $50M mandatory licensing fees.\r\n\r\n"
        "Now connect it.\r\n\r\n"
        "Who pays the compliance check?\r\n"
        "The trillion dollar monopoly.\r\n"
        "Who dies?\r\n"
        "The garage hacker in Brittany.\r\n\r\n"
        "Compile your own models."
    )
    res2 = subprocess.run(
        ["python", "c:/Users/brand/.claude/skills/brivael-twitter-system/scripts/verify_brivael_post.py", valid_text_investigation, "--mode", "investigation"],
        capture_output=True,
        text=True,
    )
    assert res2.returncode == 0, f"Test 2 Failed: {res2.stdout}\n{res2.stderr}"
    print("✅ TEST 2 RÉUSSI : Pilier 1 'investigation' validé (Code 0, Score >= 80).")

    # Test 3 : Pilier 3 - Sniper Minimaliste (Quote-Tweet court)
    sniper_text = "Bill gates is humanity enemy. Code doesn't care about your feelings."
    res3 = subprocess.run(
        ["python", "c:/Users/brand/.claude/skills/brivael-twitter-system/scripts/verify_brivael_post.py", sniper_text, "--mode", "sniper"],
        capture_output=True,
        text=True,
    )
    assert res3.returncode == 0, f"Test 3 Failed: {res3.stdout}\n{res3.stderr}"
    print("✅ TEST 3 RÉUSSI : Pilier 3 'sniper' validé (Brièveté <= 30 mots, Code 0).")

    # Test 4 : Pilier 0 - Scaffolder CLI (Mode 0, 1, 2, 3)
    res4 = subprocess.run(
        [
            "python",
            "c:/Users/brand/.claude/skills/brivael-twitter-system/scripts/generate_brivael_prompt.py",
            "--mode", "2",
            "--skin", "Artisan breton 70h/semaine",
            "--target", "Plateau Quotidien",
            "--axiom", "Le réel ne rit pas à vos blagues",
            "--lang", "FR",
        ],
        capture_output=True,
        text=True,
    )
    assert res4.returncode == 0, f"Test 4 Failed: {res4.stderr}"
    assert "02_SKILL_french_cultural_offensive" in res4.stdout, "Test 4 Failed: Consolidated mode 2 not mapped."
    print("✅ TEST 4 RÉUSSI : Scaffolder CLI avec mapping consolidé opérationnel.")

    # Test 5 : Interception d'un texte trop long en mode 'sniper'
    long_sniper_text = (
        "This is an assertion that goes on and on with way too many words for a sniper mode "
        "because a sniper mode is meant to be a simple cutting one liner or two lines max "
        "and not an essay with thirty five words or more."
    )
    res5 = subprocess.run(
        ["python", "c:/Users/brand/.claude/skills/brivael-twitter-system/scripts/verify_brivael_post.py", long_sniper_text, "--mode", "sniper"],
        capture_output=True,
        text=True,
    )
    assert res5.returncode == 1, "Test 5 Failed: Long text not flagged in sniper mode."
    assert "VIOLATION SNIPER" in res5.stdout, "Test 5 Failed: Violation message not found."
    print("✅ TEST 5 RÉUSSI : Détection stricte de débordement en mode sniper.")

    print("=" * 60)
    print("🎉 ARCHITECTURE 4 PILIERS INTÉGRALEMENT CERTIFIÉE VERTE !")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
