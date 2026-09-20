# OpenAI Codex Runtime Instructions

This file guides OpenAI Codex and ChatGPT agent environments when operating within the `ai-job-hunter` ecosystem.

## Core Directives
1. **Single Source of Truth:**
   Always reference candidate details from `reference/candidate_profile.json` and `reference/MASTER_EXPERIENCE.md`.
2. **Deterministic Pipeline:**
   - Step 1: Deduplication verification (`python3 scripts/dedupe.py --check "<Company>" "<URL>"`).
   - Step 2: Bespoke single-page LaTeX compilation using `tectonic`.
   - Step 3: Browser automation submission via Playwright with automated 8-box IMAP Gmail OTP handling.
   - Step 4: Verification screenshot & 10-field row appended to `applications.csv`.
3. **Hard Invariants:**
   - Standard hyphens only (` - `), zero unicode em-dashes (` - `).
   - Italian EU Long-Term Residence Permit (permanent resident, EU Directive 2003/109/EC mobility).
   - Accurate phone `+39 351 610 7807`.
   - No AI disclaimers in generated PDF materials.
