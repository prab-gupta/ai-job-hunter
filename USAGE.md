# AI Job Hunter: Usage Guide & Runbooks

This guide provides practical commands, execution runbooks, and slash command recipes for operating the `ai-job-hunter` plugin.

---

## 1. Quick-Start Commands

### Step 1: Run Multi-Aggregator Discovery
Discover fresh net-new postings across LinkedIn, Greenhouse, Lever, Ashby, and aggregators:
```bash
python3 scripts/sweep.py
```

### Step 2: Deduplicate a Specific Requisition
Check whether a company or URL has already been processed:
```bash
python3 scripts/dedupe.py --check "Cohere" "https://jobs.ashbyhq.com/cohere/2d256112"
```

### Step 3: Compile Bespoke LaTeX Application Materials
Compile a tailored CV and verify single-page layout:
```bash
python3 scripts/latex_builder.py --cv "Prabhavit_CV_<Company>.tex" --pages 1
```

Compile a tailored Cover Letter:
```bash
python3 scripts/latex_builder.py --letter "CoverLetter_<Company>.tex"
```

### Step 4: Reconcile Email Updates and Generate Scorecard
Sync incoming recruiter emails and generate conversion analytics:
```bash
python3 scripts/gmail_sync.py
python3 scripts/scorecard.py
```

---

## 2. Slash Command Recipes

### Start Background Autonomous Loop
To run the autonomous loop on a continuous 5-minute schedule:
```text
/schedule cron="*/5 * * * *" prompt="JOB LOOP TICK. Read STATE.md and AGENTS.md fresh. Execute 1 priority unit, update STATE.md (<=60 lines). Zero em-dashes. Screenshot before SUBMITTED."
```

### Run Overnight Target Completion
To process an entire queue of pending applications autonomously overnight:
```text
/goal Process all pending Forward Deployed Engineer and AI Engineer applications in queue.csv, compile bespoke LaTeX PDFs, submit via browser agent, log confirmations to applications.csv, and update STATE.md.
```

### Interactive Browser Application Submission
To launch the interactive browser submitter for staged portal tabs:
```text
/browser
```
Prompt:
```text
Navigate to the open ATS tabs in Chrome, fill the standard candidate profile (Prabhavit Gupta, +39 351 610 7807, prabhavitg@gmail.com, Italian EU Long-Term Resident), attach the compiled CV and Cover Letter, take confirmation screenshot into confirmations/, and log SUBMITTED to applications.csv.
```

---

## 3. Human-in-the-Loop (`NEEDS YOU`) Checklist

When the agent marks an item as `NEEDS YOU` in `STATE.md`, perform the following:
1. **Cloudflare / reCAPTCHA:** Focus the corresponding tab in Chrome, solve the puzzle, and click "Submit Application".
2. **Account Creation Walls (Workday / SAP SuccessFactors / Talentics):** Complete the one-time account login; the agent will stage all form answers and resume submission.
3. **LinkedIn 2FA / Session Verification:** If LinkedIn requests phone/email 2FA, complete the verification in Chrome.
