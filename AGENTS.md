---
framework_version: 1.0.0
---

# Universal Agent Guidelines: Autonomous AI Job Hunter

This plugin codifies the end-to-end autonomous job search, harvesting, tailoring, submission, deduplication, and outreach workflow across Gemini Antigravity, Anthropic Claude Code, and OpenAI Codex.

## 1. Thin-Pointer Design (Single Source of Truth)

To prevent duplication and configuration drift across different AI agent frameworks, all agent runtimes must load canonical candidate profiles and specifications from the plugin's `reference/` and `templates/` directories.

1. **Candidate Profile & Application Materials Policy:**
   - **LinkedIn Easy Apply:** Use the standard high-signal ATS CV (`templates/Prabhavit_CV_Base.pdf`).
   - **All Direct & Non-Easy Apply Portals:** **CUSTOM TAILORED CV & COVER LETTER ARE STRICTLY MANDATORY.** Use the LaTeX compiler pipeline (`tectonic`) to draft, tailor, and compile bespoke PDFs matching the requisition keywords, stack, and domain prior to submission.
   - **Hard Constraints:**
     - Zero em-dashes (` - ` standard only across all files, code, LaTeX, and markdown).
     - Transparent Italian EU Long-Term Residence Permit (*Permesso di Soggiorno UE per Soggiornanti di Lungo Periodo* - permanent resident, no sponsorship required in Italy or for EU remote work).
     - Accurate phone number `+39 351 610 7807`.
     - Zero AI generation disclaimers or Co-Authored-By attribution lines in submitted materials.
     - Single-page CV and single-page cover letter (enforced via `pdfinfo <file>.pdf | grep Pages` == 1).

2. **Browser & Application Execution:**
   - Use browser subagents and direct Playwright scripts with automated 8-box IMAP Gmail OTP verification for Greenhouse, and native handlers for Lever, Ashby, Workable, Personio, Recruitee, Teamtailor, and Trakstar Hire.
   - Capture confirmation screenshots into `confirmations/<company>-<date>.png` and log 10-field rows to `applications.csv`.

---

## 2. Candidate Core Facts

- **Name:** Prabhavit Gupta
- **Email:** prabhavitg@gmail.com
- **Phone:** +39 351 610 7807 (always include international prefix `+39`)
- **Location:** Venice, Italy 30175 (CET / UTC+1)
- **LinkedIn:** https://www.linkedin.com/in/prabhavit/
- **GitHub:** https://github.com/prab-gupta
- **Portfolio / Demo:** https://github.com/prab-gupta/llm-doc-parser
- **Experience:** ~3 years (Aug 2023 - Present)
- **Education:** BA Philosophy, International Studies & Economics (Minor: Entrepreneurship), Ca' Foscari University of Venice (2020 - 2024). Not a CS degree.
- **Work Authorization:**
  - Italy or EU remote performed from Italy: Authorized = Yes, Visa Sponsorship Required = No.
  - On-site outside Italy (e.g. Germany, France, Netherlands, Spain): EU Long-Term Resident Directive 2003/109/EC mobility mechanism applies.
  - UK / US / Switzerland: Authorized = No, Sponsorship Required = Yes (apply only if open to remote).
- **Salary Expectations:**
  - EUR 45,000 - 55,000 / year (Standard baseline: EUR 50,000).
  - USD 54,000 / year (USD 4,500 / month).
  - B2B / Partita IVA: EUR 250 - 300 / day.
- **Languages:** Hindi (Native), English (C2 / Bilingual), Italian (B1-B2 Conversational).
- **Active Tax Status:** Holds an active Italian Partita IVA (freelance / contract ready).

---

## 3. Claim Ladder & Technical Boundaries

- **Daily Core Production Stack (Claim with full ownership):**
  - TypeScript, JavaScript, Next.js, Node.js, Python, Laravel (PHP), PostgreSQL, Supabase.
  - Claude API, Claude Code, OpenAI API, n8n, Make, REST APIs, Webhooks, Playwright, Git/GitHub.
  - Multi-step LLM pipelines, RAG with vector retrieval, confidence-based escalation, structured data extraction.
- **Working Knowledge (Claim as working knowledge / secondary proficiency):**
  - FastAPI, Flask, Docker, Kubernetes, PyTorch (fine-tuning, embeddings, evals), Celery, Redis.
- **Strictly Off-Limits (Never claim or hallucinate):**
  - BPMN, low-level enterprise cloud admin (AWS/GCP/Azure principal architecture), computer vision, edge/embedded AI, pure ML mathematical research, fluency in German/French/Spanish.

---

## 4. Experience Weaving in Application Materials

Cover letters and tailored CVs must prominently weave all core candidate experiences:
- **FlowSpace.co:** Core real-time API connectors (OfficeRnD/Nexudus), automated listing ingestion pipeline (900+ listings), RAG support agents with confidence escalation, 99.9% uptime.
- **UltraStrategy:** AI assessment & resume optimization pipelines, multi-stage extraction scoring via Claude API & n8n.
- **Clubee:** Core API integration, automated regression test suites, QA release sign-offs.
- **Get2Germany & Urlink:** n8n automation workflows, Google API integrations, PostgreSQL indexing.
- **Featured Project:** `llm-doc-parser` (open-source asynchronous multi-agent document processing engine).

---

## 5. Deduplication & Ledger Integrity

Before taking action on any job lead:
1. Run deduplication check:
   ```bash
   python3 scripts/dedupe.py --check "<Company>" "<Job_URL>"
   ```
2. If output starts with `HIT`, do not re-apply.
3. Every submission must be appended to `applications.csv` with exactly 10 fields:
   `date,company,role,ats,url,status,confirmation_text,salary_stated,cover_letter_attached,notes`
