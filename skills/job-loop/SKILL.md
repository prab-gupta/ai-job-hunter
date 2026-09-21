---
name: job-loop
description: Run and orchestrate the continuous autonomous job application loop, tick dispatching, and state checkpointing.
---

# Job Loop Orchestrator Skill

This skill manages the active autonomous job loop. **You, the AI Agent, are the active orchestrator.** You do not need to rely on `cron` or `/schedule` background services. You will execute a continuous state machine loop to discover, analyze, tailor, and apply to jobs.

## 1. The Autonomous Agent Loop

Execute this continuous sequence using the available MCP server tools:

### Step 1: Multi-Aggregator Sweep & Harvest
- Call the `sweep_jobs` MCP tool to fetch recent high-signal job postings from ATS job boards.
- Analyze the output and queue promising roles (focusing on AI Engineer, Full-Stack, and FDE roles that are remote in the EU or based in Italy).

### Step 2: Queue Processing & Deduplication
- For each queued job, call the `dedupe_check` MCP tool with the Company Name and Job URL.
- If it returns `HIT` or already applied, discard the job and move to the next.

### Step 3: Bespoke Tailoring
- Read candidate profile from `reference/candidate_profile.json` and `reference/MASTER_EXPERIENCE.md`.
- Draft a bespoke `Prabhavit_CV_<Company>.tex` and `CoverLetter_<Company>.tex` aligning with the job description.
- Call the `compile_latex` MCP tool to generate single-page PDFs.

### Step 4: Submission
- Call the correct application MCP tool (`apply_greenhouse`, `apply_ashby`, `apply_workable`, or `apply_personio`) with the required parameters (URL, company, role, cv, letter).
- Record the submission by appending exactly 10 fields to `applications.csv`.

### Step 5: Checkpoint & Repeat
- Proceed to Step 2 (State Management).

---

## 2. State Management (`STATE.md`)

At the conclusion of every job application loop, rewrite `loop/STATE.md` to maintain a concise, real-time operating snapshot.

### Hard Constraints:
- Maximum 60 lines total.
- Use ISO-8601 or standard date timestamps.
- Divide into clear sections:
  1. `USER ACTIONS`: Manual intervention needed (CAPTCHAs, anti-AI tests, etc).
  2. `Active Submissions`: In-flight items being processed.
  3. `Confirmed Submissions This Session`: Counter and recent company list.
  4. `Standing Rules & Constraints`: Zero em-dashes, work auth summary.

---

## 3. Initiation Command

If the user simply says "start hunting" or "begin the loop", immediately enter this active, continuous background processing state and begin executing the loop steps sequentially and recursively.
