---
name: repurpose-youtube-video
description: Repurpose YouTube videos into high-converting LinkedIn, Instagram, and X (Twitter) posts with platform-optimized visuals via the Blotato API, running post log tracking, and zero-leak credential handling.
---

# Repurpose YouTube Video to Social Media Manager (Blotato Engine)

This skill acts as an autonomous AI Social Media Manager that transforms a single YouTube video URL into three distinct, platform-optimized social media posts (LinkedIn, Instagram, X/Twitter) complete with custom visuals, formatting, and live post tracking.

## Core Capabilities

1. **Content Extraction & Distillation**: Extracts key insights, framework breakdowns, hook angles, and actionable quotes from the YouTube video URL.
2. **Platform-Tailored Copywriting**:
   - **LinkedIn**: Thought-leadership essay, whitespace formatting, hook, body insights, bulleted takeaways, engagement CTA.
   - **Instagram**: High-converting carousel script or caption, visual hook, relatable storytelling, relevant hashtag cluster.
   - **X (Twitter)**: High-impact punchy post or thread hook, concise bullet points, strong one-line takeaway.
3. **Visual Generation**: Creates platform-optimized visuals (1:1 square for Instagram/LinkedIn, 16:9 or 1200x675 for X) using Blotato's visual engine.
4. **Zero-Leak Security**: Uses `BLOTATO_API_KEY` stored in `.env`. Never requests or prints the API key in conversation.
5. **Running Publication Log**: Maintains `published_posts.json` and `PUBLISHED_POSTS.md` with timestamps, platform URLs, content summaries, and asset links.
6. **Interactive Clarification Protocol**: If requirements or tone are underspecified, asks clarifying questions **one at a time** until reaching 95% confidence before running external actions.

---

## Operating Protocol

### Step 1: Environment & Secrets Check
Check if `.env` exists in the workspace. If `BLOTATO_API_KEY` is missing:
- Prompt the user: *"Veuillez renseigner votre cle API `BLOTATO_API_KEY` dans le fichier `.env` à la racine de votre projet. Ne la partagez jamais dans le chat."*
- Create a template `.env` if not present.

### Step 2: Clarification Flow (One Question at a Time)
Before generating, ask targeted questions one at a time if not specified:
- Desired brand tone (e.g., authoritative, casual, direct, educational).
- Target audience / persona.
- Specific call to action (link to newsletter, comment trigger, direct sale).

### Step 3: Video Extraction & Post Generation
Execute `scripts/blotato_client.py` or use Blotato LLM API (`https://help.blotato.com/api/llm`):
1. Extract transcript & core themes.
2. Generate copy for LinkedIn, Instagram, and X.
3. Request visual generation with platform-calibrated aspect ratios:
   - LinkedIn: 1200x1200 (Square) or 1080x1350 (Portrait)
   - Instagram: 1080x1350 (Portrait 4:5) or 1080x1080 (Square)
   - X (Twitter): 1200x675 (16:9)

### Step 4: Review & Publication
Present the drafts (Text + Visual URLs) to the user for review. Upon confirmation:
- Dispatch to connected social channels via Blotato API.
- Append published record to `published_posts.json` and update `PUBLISHED_POSTS.md`.

---

## Running Post Log Schema (`published_posts.json`)

```json
{
  "id": "post_20261024_001",
  "source_youtube_url": "https://www.youtube.com/watch?v=EXAMPLE",
  "created_at": "2026-10-24T14:30:00Z",
  "platforms": {
    "linkedin": {
      "text": "...",
      "visual_url": "https://cdn.blotato.com/...",
      "live_url": "https://linkedin.com/posts/..."
    },
    "instagram": {
      "caption": "...",
      "visual_url": "https://cdn.blotato.com/...",
      "live_url": "https://instagram.com/p/..."
    },
    "x": {
      "text": "...",
      "visual_url": "https://cdn.blotato.com/...",
      "live_url": "https://x.com/user/status/..."
    }
  }
}
```