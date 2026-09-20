---
name: job-loop
description: Run and orchestrate the continuous autonomous job application loop, tick dispatching, and state checkpointing.
---

# Job Loop Orchestrator Skill

This skill manages the autonomous background job loop, scheduling periodic executions, managing priorities across application queues, and writing atomic checkpoints.

## 1. Loop Lifecycle & Scheduling

The job loop runs on a recurring schedule (e.g. every 5 minutes via `/schedule` or cron `*/5 * * * *`).

### Tick Execution Order (Strict Precedence):
1. **08:00 Morning Check:** Check Gmail replies if last check was >24h ago; sync incoming recruiter replies to `loop/gmail_threads.jsonl`.
2. **Queue Processing (Priority 1):** If `queue.csv` contains rows with status `TO APPLY`:
   - Pick the highest priority row (e.g., FDE or direct ATS application).
   - Generate bespoke LaTeX CV and Cover Letter via `cv-tailor`.
   - Submit via `browser-apply`.
   - Update `queue.csv` and `applications.csv`.
3. **LinkedIn Harvesting (Every 3rd Tick):** Run LinkedIn harvesting unit for 24-hour job postings (focus on Italy and EU remote FDE / AI roles).
4. **Hourly Multi-Aggregator Sweep:** Run `python3 scripts/sweep.py` across ATS job boards (Greenhouse, Lever, Ashby, FreeHire) to gate fresh candidates into `queue.csv`.
5. **Outreach Unit (Every 2nd Tick Mon-Fri 08:00-19:00):** Process cold outreach leads and draft personalized email pitches.
6. **Idle Tick:** If no actionable tasks exist, log a single-line heartbeat.

---

## 2. State Management (`STATE.md`)

At the conclusion of every tick, rewrite `STATE.md` to maintain a concise, real-time operating snapshot.

### Hard Constraints:
- Maximum 60 lines total.
- Use ISO-8601 or standard date timestamps (`date` command).
- Divide into clear sections:
  1. `USER ACTIONS`: Unblockable manual tasks (CAPTCHAs, account logins, anti-AI tests).
  2. `Active Submissions`: In-flight items being processed.
  3. `Confirmed Submissions This Session`: Counter and recent company list.
  4. `Standing Rules & Constraints`: Zero em-dashes, work auth summary.

---

## 3. Slash Command Triggers

- Start continuous background loop:
  `/schedule cron="*/5 * * * *" prompt="JOB LOOP TICK. Read STATE.md and AGENTS.md fresh. Execute 1 priority unit, update STATE.md (<=60 lines). Zero em-dashes."`
- Run one bounded overnight cycle:
  `/goal Apply to all pending FDE and AI Engineer roles in queue.csv, compile bespoke LaTeX PDFs, and report final confirmation stats.`
