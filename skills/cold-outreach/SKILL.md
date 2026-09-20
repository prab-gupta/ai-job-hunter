---
name: cold-outreach
description: Generate localized, high-conversion cold outreach emails and LinkedIn connection notes for hiring managers and founders.
---

# Cold Outreach Skill

This skill handles direct candidate outreach to founders, engineering directors, and talent leads across European tech companies.

## 1. Operating Rules & Guardrails

1. **Send Window:** Mon-Fri 08:00 - 21:00 Europe/Rome (CET).
2. **Cap:** Maximum 20 emails per day.
3. **Target Emails:** Sent only to publicly published email addresses on the company's verified domain (`careers@`, `jobs@`, or named founder/executive).
4. **Follow-Up Policy:** Exactly one polite follow-up at +7 business days.
5. **Attachments:** Attach standard comprehensive CV (`Prabhavit_CV_Original_EN.pdf` or `Prabhavit_CV_Standard.pdf`).
6. **Logging:** Log every outgoing outreach in `loop/outreach.csv` with the target source URL.

---

## 2. Localization & Tone

- **English Outreach (European / Global companies):**
  - Crisp, concise, outcome-driven, British or neutral English.
  - Structure: Personal hook + Relevant technical proof (2 roles) + Live demo link + Clear low-friction CTA.
- **Italian Outreach (Italian companies / local founders):**
  - Natural, professional Italian.
  - Use formal-friendly plural "voi" to the engineering team; "tu" only to startup founders in early-stage teams.
  - Draw directly from `reference/MASTER_EXPERIENCE.md` Italian summary block.

---

## 3. LinkedIn Connection Notes

- Max 300 characters total.
- Highlight specific relevant tech match (e.g. Next.js, LLM document parsing, FlowSpace migration, n8n).
- Include GitHub demo: `github.com/prab-gupta/llm-doc-parser`.
- Output daily ready-to-send batch to `outreach/linkedin-<date>.md`.
