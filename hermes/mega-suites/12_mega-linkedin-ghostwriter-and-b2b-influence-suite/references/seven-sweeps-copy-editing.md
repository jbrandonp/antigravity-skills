# The Seven Sweeps Method of Copy-Editing for LinkedIn

Inspired by Corey Haines (*MarketingSkills*) and the *Smol Architect* standards, the **Seven Sweeps** is a sequential editing protocol. Trying to fix clarity, voice, rhythm, formatting, and AI slop in a single pass leads to overlooked errors. Execute each sweep focused strictly on one dimension.

---

## The 7 Sequential Sweeps

```
Sweep 1: Clarity & Logic        (Does every paragraph logically require the next?)
Sweep 2: Voice & Authority      (Kill corporate stiffness; speak peer-to-peer)
Sweep 3: Rhythm & Burstiness    (Mix 4-word punchlines with 18-word mechanisms)
Sweep 4: Verbs & Active Voice   (Zombie Test: replace passive constructions)
Sweep 5: Anti-Slop & AI Tells   (Eradicate false opposites, filler words & buzzwords)
Sweep 6: Mobile Fold Geometry   (Cut tension before char 210; clean breathing space)
Sweep 7: Falsifiability & Data  (Replace vague adjectives with verified numbers)
```

---

### Sweep 1: Clarity & Logic (The Coherence Test)
- **Question:** If a paragraph were deleted, would the argument collapse? If not, delete it.
- **Rule:** One single core thesis per post. If you find two insights, split them into two separate drafts.
- **Transition Check:** Replace abrupt jumps with cause-and-effect transitions (*"Because of this"*, *"And that broke our assumption"*).

---

### Sweep 2: Voice & Authority (The Peer Tone)
- **Question:** Does this sound like a senior practitioner talking to an equal at a coffee shop, or like an official press release?
- **Rule:** Banish corporate modesty (*"I am humbled to announce"*) and false excitement (*"Thrilled to share!"*).
- **Attitude:** Understated competence. Confident, direct, calm.

---

### Sweep 3: Rhythm & Burstiness (The Staccato Balance)
- **Question:** Are all sentences the same length (12–15 words)? If yes, it sounds like an LLM.
- **Rule:** Standard deviation of sentence length must be $\sigma \ge 3.5$ words.
- **Pattern:**
  > *We tested 4 scrapers.* (4 words)  
  > *None of them survived the new Cloudflare TLS fingerprinting challenge.* (10 words)  
  > *When we decrypted the incoming client hello frames, we discovered the edge proxy was comparing our cipher suites against known headless browser signatures.* (22 words)  
  > *That changed everything.* (3 words)

---

### Sweep 4: Verbs & Active Voice (The Zombie Test)
- **Question:** Can you insert *"by zombies"* after the verb? If yes, it is passive voice.
  - *Example:* *"The database was locked [by zombies]"* $\rightarrow$ **Active:** *"The unindexed migration locked the database."*
- **Action:** Convert nominalizations into strong verbs:
  - *Weak:* *"We conducted an optimization of the queries."*
  - *Strong:* *"We optimized the queries."*

---

### Sweep 5: Anti-Slop & AI Tells Purge
- **Checklist:**
  - Strip *"It's not just X, it's Y"* or *"Il ne s'agit pas de X, mais de Y"*.
  - Strip empty openers (*"In today's fast-paced digital world"*, *"Dans un monde où"*).
  - Strip listicle meta-announcements (*"Here's why:"*, *"Voici pourquoi :"*, *"Let's dive in"*).
  - Strip arrogant mic-drop closers (*"Read that again."*, *"Let that sink in."*).

---

### Sweep 6: Mobile Fold Geometry & Whitespace
- **Checklist:**
  - Measure characters before the first double linebreak. Must be **$\le 210$ characters** (optimally 140–180 chars).
  - No dense 8-line blocks of unbroken text.
  - No 1-sentence paragraph spam ("broetry"). Group thoughts in 2-3 logical lines.

---

### Sweep 7: Falsifiability & Ground Truth Data
- **Question:** Could this claim be proven false with real numbers?
  - *Fluff:* *"We achieved massive latency improvements."* (Unfalsifiable)
  - *Data:* *"We cut p99 latency from 1,420ms to 84ms on 10,000 concurrent requests."* (Falsifiable)
- **Placeholder Rule:** If the exact number is private or missing, write `{{your latency metric}}` instead of inventing a plausible statistic.
