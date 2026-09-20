# Gemini Antigravity & Gemini CLI Runtime Instructions

This file guides the Google Gemini CLI and Antigravity agents when operating within the `ai-job-hunter` ecosystem.

## Discovery & Skills
Antigravity automatically discovers skills defined in `skills/*/SKILL.md`.

### Core Commands & Procedures
1. **Deduplication Check:**
   ```bash
   python3 scripts/dedupe.py --check "<Company>" "<Job_URL>"
   ```
2. **Tailoring Materials (Tectonic LaTeX):**
   - Read candidate profile from `reference/candidate_profile.json` and `reference/MASTER_EXPERIENCE.md`.
   - Create single-page `Prabhavit_CV_<Company>.tex` and `CoverLetter_<Company>.tex`.
   - Compile:
     ```bash
     python3 scripts/latex_builder.py --cv "Prabhavit_CV_<Company>.tex"
     python3 scripts/latex_builder.py --letter "CoverLetter_<Company>.tex"
     ```
   - Verify page counts: both must be exactly 1 page (`pdfinfo <file>.pdf | grep Pages` == 1).
3. **Browser Form Submission:**
   - For Greenhouse: Execute `scripts/apply_greenhouse.py` with automatic 8-box IMAP Gmail OTP verification.
   - For Ashby: Execute `scripts/apply_ashby.py`.
   - For Personio / Workable / Teamtailor / Trakstar: Execute corresponding submitter script.
   - Capture confirmation screenshot to `confirmations/<Company>-<Date>.png`.
4. **Ledger Recording:**
   - Append exact 10-field row to `applications.csv`:
     `date,company,role,ats,url,status,confirmation_text,salary_stated,cover_letter_attached,notes`
5. **State Management:**
   - Keep `loop/STATE.md` strictly under 60 lines.

## Hard Constraints
- Zero em-dashes (` - ` only).
- Transparent Italian EU Long-Term Residence Permit (permanent resident, zero sponsorship needed in Italy or EU remote).
- Accurate phone `+39 351 610 7807`.
- Zero AI generation disclaimers or Co-Authored-By lines in submitted materials.
