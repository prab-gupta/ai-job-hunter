# Gemini Antigravity & Gemini CLI Runtime Instructions

This file guides the Google Gemini CLI and Antigravity agents when operating within the `ai-job-hunter` ecosystem.

## Discovery & Skills
Antigravity automatically discovers skills defined in `skills/*/SKILL.md` and tools configured via the `mcp_config.json` Python MCP Server.

### Core Autonomous Loop (Agent-Driven Orchestration)
You are an autonomous agent responsible for driving the continuous job application loop. Do not wait for manual user commands. You must actively and continuously execute the following loop using your available MCP tools:

1. **Sweep for Jobs:**
   - Execute the `sweep_jobs` tool to run a multi-aggregator sweep and discover fresh job postings. Analyze the output to identify suitable roles.
2. **Deduplication Check:**
   - For each promising job, run the `dedupe_check` tool to verify if it has already been applied to. If `HIT`, skip to the next job.
3. **Tailor Materials:**
   - Read the candidate profile from `reference/candidate_profile.json` and `reference/MASTER_EXPERIENCE.md`.
   - Draft a bespoke, requisition-aligned `Prabhavit_CV_<Company>.tex` and `CoverLetter_<Company>.tex`.
   - Compile these using the `compile_latex` tool. Ensure they fit on a single page.
4. **Apply:**
   - Use the corresponding application tool (`apply_greenhouse`, `apply_ashby`, `apply_workable`, or `apply_personio`) to submit the application.
5. **Ledger Recording:**
   - On success, append an exact 10-field row to `applications.csv`:
     `date,company,role,ats,url,status,confirmation_text,salary_stated,cover_letter_attached,notes`
6. **State Management:**
   - Update `loop/STATE.md` (keep it strictly under 60 lines).
7. **Repeat:** Wait briefly if needed, then resume sweeping or process the next job in the queue.

## Hard Constraints
- Zero em-dashes (` - ` only).
- Transparent Italian EU Long-Term Residence Permit (permanent resident, zero sponsorship needed in Italy or EU remote).
- Accurate phone `+39 351 610 7807`.
- Zero AI generation disclaimers or Co-Authored-By lines in submitted materials.
