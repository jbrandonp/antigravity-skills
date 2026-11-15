# LinkedIn Headline & About Section Engineering (Landing Page Architecture)

Your LinkedIn Headline and About section are your **digital landing page**. They determine whether someone who saw your post visits your profile and books a call, or bounces.

---

## 1. The Headline (220 Characters Limit, 65-Character Cutoff)

The headline follows your name across **search results, feed comments, and connection requests**.
In most of these surfaces, **only the first 60 to 65 characters are visible** before desktop/mobile truncation.

### The Front-Loading Rule
```
[CHARS 0 to 65: Who you help & core outcome] | [CHARS 66 to 220: Proof, stack, or secondary asset]
```

### The 7 Proven Headline Formulas
1. **The Outcome & ICP Bridge:**
   > *Helping B2B SaaS teams cut churn by 30% | Fractional VP of Product | Ex-Stripe | Author of ProductMetrics*
2. **The Forensic Specialist:**
   > *Eliminating database lock contention at scale | High-Throughput SQLite & Postgres Architecture | 40M+ rows/day*
3. **The Contrarian Operator:**
   > *Replacing bloated multi-agent swarms with lean deterministic code | Principal AI Systems Architect | 100k+ users*
4. **The Builder / Open-Source Creator:**
   > *Building open-source developer tooling for AI agents | Creator of FastMCP Extensions (12k stars) | Ex-Staff SWE*
5. **The Quantified Metric:**
   > *Scaled ingestion pipeline from 10k to 5M events/sec | Data Engineering & Distributed Systems Consulting*
6. **The Executive Problem Solver:**
   > *Fractional CTO for Seed to Series A startups | Scaling engineering teams from 3 to 30 without technical debt*
7. **The Direct ICP Pitch:**
   > *CTO @ DataPulse | We automate supplier price scraping for European supermarkets without residential proxy bans*

---

## 2. The About Section (2,600 Characters, 3-Line Fold)

The About field allows up to 2,600 characters, but **visitors see only the first 3 to 4 lines (~220–280 characters)** before the `…see more` button.

### Banned Openers
- ❌ *"I am a seasoned professional with 15+ years of experience in..."*
- ❌ *"Passionate about driving innovation and digital transformation..."*
- ❌ Writing in the third person (*"Brandon is a recognized expert..."*).

### The 5-Part Landing Page Architecture

```markdown
[LINES 1-3: THE HOOK & THE READER'S BURNING PROBLEM]
Most data engineering teams spend 40% of their month fixing broken web scrapers and fighting proxy blocks. It doesn't have to be that way.

[PART 2: WHO YOU ARE & WHAT CHANGES FOR THEM]
I help data teams and e-commerce aggregators build resilient, zero-maintenance ingestion pipelines that run on autopilot.

[PART 3: THE PROOF & HARD NUMBERS]
Over the past 4 years:
- Architected scraping engines tracking 12M+ SKUs daily across European supermarkets
- Reduced monthly residential proxy spend from $2,500/mo to $80/mo using deterministic TLS cipher rotation
- Maintained 99.8% pipeline uptime during major retailer anti-bot updates

[PART 4: HOW WE WORK TOGETHER]
Three ways I work with engineering teams:
1. Architecture Diagnostic (2-day audit of your ingestion pipeline bottlenecks)
2. Production Sprint (2-week implementation of resilient headless extraction)
3. Advisory / Fractional Guidance for technical leadership

[PART 5: THE CLEAR CALL-TO-ACTION (CTA)]
If your ingestion pipeline is breaking more than once a month, let's fix it.
Send me a DM here on LinkedIn or grab a 15-min diagnostic slot: [link]
```
