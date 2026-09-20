---
name: browser-apply
description: Autonomous browser-based job application submitter for Greenhouse, Lever, Ashby, Workable, Personio, Recruitee, Teamtailor, and LinkedIn Easy Apply.
---

# Browser Application Submitter Skill

This skill executes form filling and application submission via Chrome browser tools (`/browser`, Chrome sidecar, and ref-based selectors).

## 1. Supported ATS Platforms & Operational Rules

| ATS Platform | Target Form Pattern | Specific Quirks / Instructions |
|---|---|---|
| **Greenhouse** | `job-boards.greenhouse.io/<co>/jobs/<id>` | Auto-attach CV + Cover Letter; decline optional demographic surveys. Solve Turnstile/reCAPTCHA if present. |
| **Lever** | `jobs.lever.co/<co>/<id>/apply` | Ref-based input filling. Paste tailored cover letter into text box or upload file. |
| **Ashby** | `jobs.ashbyhq.com/<co>/<id>` | Location autocomplete requires explicit selection click. Real keystrokes required on input fields. |
| **Workable** | `apply.workable.com/<co>/j/<id>/apply` | Re-verify address and phone after CV upload parsed. |
| **Personio** | `<co>.jobs.personio.de/job/<id>/apply` | Multi-file upload slots for CV and Motivation Letter. |
| **Recruitee** | `<co>.recruitee.com/o/<id>/c/new` | Direct apply page is `/c/new`. Fill standard candidate profile. |
| **Teamtailor** | `<co>.teamtailor.com/jobs/<id>` | One-click apply modal. Autofill profile fields. |
| **LinkedIn Easy Apply** | `/jobs/view/<id>/` | Tab must be foregrounded (`document.visibilityState === "visible"`). Upload tailored CV PDF. |

---

## 2. Standard Candidate Form Answers

- **First Name:** Prabhavit
- **Last Name:** Gupta
- **Email:** prabhavitg@gmail.com
- **Phone:** +39 351 610 7807 (local number: `3516107807` if country code is separate)
- **Location / City:** Venice, Italy (or Venice, Veneto, Italy)
- **Postal Code:** 30175
- **LinkedIn URL:** https://www.linkedin.com/in/prabhavit/
- **GitHub URL:** https://github.com/prab-gupta
- **Portfolio / Website:** https://github.com/prab-gupta/llm-doc-parser
- **Years of Experience:** 3 (integer)
- **Work Authorization:**
  - *Are you legally authorized to work in Italy / EU Remote?* **Yes**
  - *Will you now or in the future require visa sponsorship?* **No** (for Italy / EU Remote)
  - *Visa status:* Italian EU Long-Term Residence Permit (*Permesso di Soggiorno UE per Soggiornanti di Lungo Periodo* - permanent resident).
- **Desired Salary:** EUR 50,000 / year (or USD 54,000 / year).
- **Notice Period / Availability:** Immediately / 0 days.

---

## 3. Human-in-the-Loop Hand-off Policy (`NEEDS YOU`)

If any of the following are encountered, the agent must fill all available standard fields, pause submission, and log the row as `NEEDS YOU` in `STATE.md`:
1. CAPTCHA / Cloudflare Turnstile puzzle requiring human interaction.
2. Account creation / password registration walls (e.g. Workday, SAP SuccessFactors, Talentics).
3. Anti-AI screening questionnaires or "I certify no AI was used" attestations.
4. Video interview recordings or one-way video prompts.
