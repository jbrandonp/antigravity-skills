# LinkedIn Character Limits & Surface Visibility Guide (2026 Edition)

A comprehensive reference for character limits, input maximums, and visual truncation points across all LinkedIn surfaces.

---

## 1. Complete Surface Limits Table

| Surface / Field | Hard Limit | Visibility Fold / Cutoff | Optimal Target Length | Strategic Rule |
| :--- | :--- | :--- | :--- | :--- |
| **Post Body** | 3,000 chars | ~140 chars (mobile)<br>~210 chars (desktop) | 900–1,300 chars | Hook must create tension *before* the `...see more` fold. |
| **Headline** | 220 chars | ~60–65 chars (search & comments) | 180–210 chars | Front-load primary ICP & outcome into the first 65 characters. |
| **About / Summary** | 2,600 chars | ~220–280 chars (3–4 lines) | 1,200–1,600 chars | Treat as a landing page. Lead with reader's problem, not bio. |
| **Connection Note** | 200 chars (standard) | Fully visible | 120–180 chars | Never pitch. Context + observation + clean invite ask. |
| **Direct Message (DM)** | 8,000 chars | ~250 chars (preview notification) | 200–600 chars | 1 specific question or asset drop. Short paragraphs. |
| **Comment** | 1,250 chars | ~120 chars | 150–350 chars | Add data or contrarian nuance; avoid 1-word generic praises. |
| **Poll Question** | 140 chars | Fully visible | 60–90 chars | Clear, thought-provoking question provoking debate. |
| **Poll Option** | 30 chars | Fully visible | 15–25 chars | Exactly 3 or 4 mutually exclusive choices. |
| **Article Headline** | 100 chars | Fully visible | 50–70 chars | High SEO & curiosity clarity. |
| **Article Body** | 120,000 chars | Paged / Scroll | 4,000–8,000 chars | Long-form cornerstone guide. |
| **Experience Bullet** | 2,000 chars | 5 lines per role | 400–600 chars | Quantified outcomes over listed duties. |
| **Recommendation** | 3,000 chars | Fully visible | 500–800 chars | Concrete projects, numbers delivered, and team impact. |
| **Company Page Tagline** | 120 chars | Fully visible | 80–110 chars | One-sentence company positioning statement. |
| **Company Page About** | 2,000 chars | ~200 chars | 800–1,200 chars | Customer problem $\rightarrow$ solution $\rightarrow$ career link. |

---

## 2. Terminal Quick-Check Formulas

- **Mobile Hook Verification:**
  ```python
  first_paragraph = text.split("\n\n")[0]
  assert len(first_paragraph) <= 210, "Hook will be cut mid-sentence on mobile!"
  ```
- **Connection Note Verification:**
  ```python
  assert len(note) <= 200, "Connection note exceeds 200 characters limit!"
  ```
- **Poll Validation:**
  ```python
  assert len(question) <= 140, "Poll question exceeds 140 chars!"
  for option in options:
      assert len(option) <= 30, f"Poll option '{option}' exceeds 30 chars!"
  ```
