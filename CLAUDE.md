# Claude Code Runtime Instructions

This file guides Anthropic Claude Code when operating within the `ai-job-hunter` ecosystem.

## Canonical Thin-Pointer Architecture
All candidate specifications, experiences, and rules are maintained in `reference/` and `templates/`. Treat them as single sources of truth.

## Standard Workflows & Commands

### 1. Tailoring Application Materials (`/tailor`)
- Read target job requisition requirements, stack, and domain.
- Load `reference/candidate_profile.json` and `reference/MASTER_EXPERIENCE.md`.
- Weave candidate experiences (FlowSpace.co, UltraStrategy, Clubee, Get2Germany, Urlink, and `llm-doc-parser`).
- Generate bespoke `Prabhavit_CV_<Company>.tex` and `CoverLetter_<Company>.tex`.
- Compile via tectonic:
  ```bash
  tectonic "Prabhavit_CV_<Company>.tex" && tectonic "CoverLetter_<Company>.tex"
  ```
- Verify 1-page constraints:
  ```bash
  pdfinfo "Prabhavit_CV_<Company>.pdf" | grep Pages
  pdfinfo "CoverLetter_<Company>.pdf" | grep Pages
  ```

### 2. Form Submissions (`/apply`)
- Run deduplication check:
  ```bash
  python3 scripts/dedupe.py --check "<Company>" "<Job_URL>"
  ```
- If `NEW`, proceed to browser submission using Playwright or native submitters with automated Greenhouse 8-box OTP resolution.
- Save confirmation screenshot into `confirmations/<Company>-<Date>.png`.
- Record 10-field row in `applications.csv`.

### 3. Loop Checkpointing (`/loop`)
- Execute one unit per tick (harvest -> tailor -> submit -> ledger).
- Rewrite `loop/STATE.md` (strictly <= 60 lines).

## Strict Invariants
- 0 em-dashes across all files (` - ` standard hyphens only).
- Transparent Italian EU Long-Term Residence Permit (*Permesso di Soggiorno UE per Soggiornanti di Lungo Periodo*).
- Phone: `+39 351 610 7807`.
- No AI generation disclaimers or Co-Authored-By attribution lines in output materials.
