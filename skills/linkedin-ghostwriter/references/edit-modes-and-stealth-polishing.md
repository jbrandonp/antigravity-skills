# Editing Modes & Stealth De-Slop Polishing

How to polish existing drafts without stripping the author's authentic voice, and how to eliminate the most subtle, telltale AI formatting patterns.

---

## 1. The 3 Editing Modes

Before editing any text, diagnose which mode applies:

| Mode | Input Signs | Prescribed Action | Scope of Edits |
| :--- | :--- | :--- | :--- |
| **Mode A: Blank or Slop** | Generic company-speak, AI mush, zero point of view, buzzwords. | **Full Rebuild:** Reconstruct sentences from underlying facts. Interview for real metrics. | All 7 sweeps. Rebuild sentences. Never hallucinate data. |
| **Mode B: Real Voice** | A clear opinion, rough grammar, distinct vocabulary, authentic experience. | **Restoration:** Preserve author's exact argument, vocabulary, and rhythm. Fix the buried lede and mobile fold. | Tighten phrasing, clean linebreaks, remove accidental slop. Keep their personality. |
| **Mode C: Point Edit** | *"Fix this hook"*, *"Is this sentence OK?"*, *"Tighten paragraph 2"*. | **Surgical Fix:** Change only the target line and the minimum context around it (a pronoun, a transition). | Skip the full report. Return changed line with a 1-line reason + 1 alternative. |

---

## 2. The Subtle AI Formatting Tells (And How to Fix Them)

Beyond obvious buzzwords like *"delve"* or *"catalyseur"*, advanced readers and algorithmic classifiers look for structural patterns:

### Tell 1: Bold Labels on Every Bullet
- **The AI Tell:**
  > - **Clarity:** We clean the logs.  
  > - **Efficiency:** We drop slow queries.  
  > - **Simplicity:** We use SQLite.
- **The Human Fix:** Integrate the concept naturally into the sentence:
  > - We clean the logs every 24 hours.  
  > - We terminate queries exceeding 500ms.  
  > - We store state in a single local SQLite file.

### Tell 2: Staged Reveal Openers
- **The AI Tell:** *"Picture this:"*, *"Let's face it:"*, *"Here's the thing:"*, *"Spoiler alert:"*.
- **The Human Fix:** Delete the staged line entirely. Start with the fact itself.

### Tell 3: Inflated Significance Clichés
- **The AI Tell:**
  - FR: *"témoigne de"*, *"un rappel cuisant que"*, *"ouvre la voie à"*, *"force est de constater"*.
  - EN: *"serves as a testament to"*, *"a stark reminder that"*, *"paves the way for"*, *"underscores the importance of"*.
- **The Human Fix:** State the cause and effect directly without melodrama.

### Tell 4: The 1-Word Mic-Drop Closer
- **The AI Tell:** *"Thoughts?"*, *"Agree?"*, *"Read that again."*, *"Let that sink in."*.
- **The Human Fix:** Ask an informed, technical question that only someone with real experience in the field could ask.
