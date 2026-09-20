---
framework_version: 1.0.0
---

# Agent Guidelines: Autonomous AI Job Hunter

This plugin codifies the end-to-end autonomous job search, harvesting, tailoring, submission, deduplication, and outreach workflow.

## 1. Thin-Pointer Design (Single Source of Truth)

To prevent duplication and configuration drift across different AI agent frameworks (Antigravity, Claude Code, Gemini CLI, Cursor, Codex), all agent runtimes must load canonical candidate profiles and specifications from the plugin's `reference/` and `templates/` directories.

1. **Candidate Profile & Application Materials Policy:**
   - **LinkedIn Easy Apply:** Use the standard high-signal ATS CV (`templates/Prabhavit_CV_Base.pdf` / `Prabhavit_CV_Standard.pdf`).
   - **All Direct & Non-Easy Apply Portals:** **CUSTOM TAILORED CV & COVER LETTER ARE STRICTLY MANDATORY.** Use the LaTeX compiler pipeline (`tectonic`) to draft, tailor, and compile bespoke PDFs matching the requisition keywords, stack, and domain prior to submission.
   - **Hard Constraints:**
     - Zero em-dashes (` - ` standard only across all files, code, and markdown).
     - Transparent Italian EU Long-Term Residence Permit (*Permesso di Soggiorno UE per Soggiornanti di Lungo Periodo* - permanent resident, no sponsorship required in Italy or for EU remote work).
     - Accurate phone number `+39 351 610 7807`.
     - Zero AI generation disclaimers or Co-Authored-By attribution lines in submitted materials.

2. **Browser & Application Execution:**
   - No standalone brittle scripts. Use browser subagents and direct Chrome tools (`/browser`, Chrome sidecar / extension) exclusively for all browser interactions, form filling, and job applications.
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

## 4. Gating & Filtering Rules

1. **Target Tracks:**
   - **Track A:** AI / Automation Engineer (LLM pipelines, agents, workflow automation).
   - **Track B:** Forward Deployed Engineer (FDE), Solutions Engineer, Technical Account Manager, Implementation Engineer.
   - **Track C:** Full-Stack Engineer, Product Engineer.
   - **Track D:** Technical Project Manager, GTM Engineer, DevRel, QA Automation.
2. **Hard Exclusions (Kill immediately):**
   - Requires >3 years of experience (Junior, Mid, and <=3 YoE accepted; Mid-Senior accepted if stack aligns).
   - Hard requirement for MSc/PhD in Computer Science or specialized ML research background.
   - Mandatory fluent German, French, Polish, Dutch, or Spanish without English option.
   - Unnamed agencies, talent pools, or reposters (e.g., Scale Army, Remote Recruitment, Hire Feed, FetchJobs).
   - Roles located exclusively on-site in the US or UK without remote flexibility.
3. **LinkedIn Special Gating:**
   - For all LinkedIn Forward Deployed Engineer (FDE) postings in Italy and the EU: **PRIORITY DISPATCH**. Apply immediately with bespoke materials.
   - For LinkedIn Top Job Picks / Recommendations: Soft gates are relaxed. Apply with tailored materials unless closed, duplicate, or language-blocked.

---

## 5. Deduplication & Ledger Integrity

Before taking action on any job lead:
1. Run deduplication check:
   ```bash
   python3 scripts/dedupe.py --check "<Company>" "<Job_URL>"
   ```
2. If output starts with `HIT`, do not re-apply.
3. Reconcile company aliases (e.g., "MAU / AI-LAB" maps to "Leadtech", "Transcendent Group" maps to "Advisense").
4. Every submission must be appended to `applications.csv` with exactly 10 fields:
   `date,company,role,ats,url,status,confirmation_text,salary_stated,cover_letter_attached,notes`

---

## 6. Status Vocabulary

Only the following standard statuses may be used in tracking files (`STATE.md`, `applications.csv`, `queue.csv`):
- `SUBMITTED`: Form fully completed and verified with on-screen confirmation and screenshot.
- `TO APPLY`: Materials generated, ready for browser automation submission.
- `NEEDS YOU`: Blocked by CAPTCHA, SMS 2FA, video answer, or manual account creation wall.
- `BLOCKED`: Technical issue preventing submission.
- `DROPPED`: Disqualified after deep JD review.
- `CLOSED`: Job requisition expired or unlisted.
- `DEAD`: Company unresponsive or requisition cancelled.
- `SKIP - <reason>`: Explicitly skipped with documented rationale.
- `REPLIED`: Company acknowledged or reached out.
- `INTERVIEW`: Screening or technical interview scheduled.
- `REJECTED`: Formal rejection notice received.
