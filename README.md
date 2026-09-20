# 🚀 AI Job Hunter: Universal Autonomous Agent Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platforms](https://img.shields.io/badge/Frameworks-Gemini%20Antigravity%20%7C%20Claude%20Code%20%7C%20OpenAI%20Codex-brightgreen.svg)]()
[![Automation](https://img.shields.io/badge/Engine-Playwright%20%2B%20Tectonic%20%2B%20LangGraph-orange.svg)]()

An autonomous, multi-agent AI job search, bespoke tailoring, verification, deduplication, and application submission system designed to operate natively across **Google Antigravity / Gemini CLI**, **Anthropic Claude Code**, and **OpenAI Codex**.

---

## 🌟 Key Highlights & Capabilities

- **Universal Multi-Framework Architecture:** Thin-pointer design that mounts identically across Antigravity (`.agents/`), Claude Code (`.claude/`), and OpenAI Codex (`.codex/`).
- **Bespoke LaTeX CV & Cover Letter Compiler:** Compiles requisition-aligned single-page PDFs in sub-seconds using `tectonic`, validating layout and zero em-dash compliance.
- **Automated Greenhouse 8-Box OTP Resolution:** End-to-end IMAP email verification solver for modern split-token Greenhouse anti-bot verification.
- **Native Browser Submitters:** Robust Playwright handlers for Greenhouse, Lever, Ashby (with Turnstile support), Personio, Workable (with auto-fill protection), Recruitee, Teamtailor, and Trakstar Hire (`?apply=true` direct bypass).
- **Canonical 10-Field Ledger & Deduplication:** Bulletproof URL normalization, company alias mapping, and strict CSV schema validation.
- **Multi-Aggregator Harvesting:** Scrapes and normalizes high-signal tech roles across FreeHire, LinkedIn, Ashby, Greenhouse, and European job platforms.
- **Automated Checkpointed Loop:** Continuous autonomous state machine maintaining `loop/STATE.md` under 60 lines.

---

## 📁 Repository Structure

```
ai-job-hunter/
├── plugin.json                 # Gemini Antigravity / Gemini CLI Manifest
├── AGENTS.md                   # Universal Thin-Pointer Agent Guidelines
├── GEMINI.md                   # Google Gemini / Antigravity System Context
├── CLAUDE.md                   # Anthropic Claude Code System Context
├── CODEX.md                    # OpenAI Codex System Context
├── mcp_config.json             # MCP Server Config for Agent Runtimes
├── README.md                   # Project Overview & Architecture
├── USAGE.md                    # Quick-Start Command Reference
├── INSTALL.md                  # Multi-Platform Setup Guide
├── LICENSE                     # MIT License
├── reference/                  # Canonical Knowledge Base
│   ├── candidate_profile.json  # Machine-readable candidate core facts
│   ├── MASTER_EXPERIENCE.md    # Detailed work history & project achievements
│   ├── CLAIM_LADDER.md         # Production stack vs working knowledge vs off-limits
│   ├── ATS_QUIRKS.md           # Field mappings, OTP solvers & form quirks
│   └── CANNED_ANSWERS.md       # Standard responses for salary, notice, permit
├── templates/                  # Base Single-Page LaTeX & Outreach Templates
│   ├── Prabhavit_CV_Base.tex   # Single-page modern ATS LaTeX CV template
│   ├── CoverLetter_Base.tex    # Single-page high-conversion Cover Letter template
│   ├── photo.jpg               # Candidate profile photograph
│   └── DM-templates.md         # LinkedIn & cold email outreach templates
├── skills/                     # Modular Skill Definitions
│   ├── cv-tailor/              # Bespoke LaTeX tailoring & single-page compiler
│   ├── browser-apply/          # Autonomous browser submitter with OTP solver
│   ├── job-sweep/              # Multi-aggregator job harvester & filter
│   ├── dedupe-tracker/         # Deduplication engine & 10-field ledger integrity
│   ├── job-loop/               # Continuous autonomous scheduled loop
│   ├── cold-outreach/          # Multi-lingual founder & recruiter outreach
│   └── interview-prep/         # Architecture deep-dives & live coding prep
├── rules/                      # Enforced Agent Constraints
│   ├── AGENTS.md               # Universal thin-pointer guidelines
│   ├── ZERO_EM_DASH.md         # Strict ASCII hyphen enforcement
│   └── LEDGER_INTEGRITY.md     # 10-field CSV schema and dedupe rules
├── .claude/                    # Claude Code specific commands & configs
│   └── commands/               # /tailor, /apply, /sweep, /loop
├── .codex/                     # OpenAI Codex specific tool definitions
│   └── config.json
└── scripts/                    # Core Python Automation Scripts
    ├── apply_greenhouse.py     # Greenhouse submitter with automated 8-box IMAP OTP
    ├── apply_ashby.py          # Ashby submitter with Turnstile handling
    ├── apply_personio.py       # Personio submitter with GDPR consent handling
    ├── apply_workable.py       # Workable submitter with auto-fill preservation
    ├── latex_builder.py        # Tectonic LaTeX compiler & 1-page validator
    ├── dedupe.py               # Canonical deduplication check & ledger sync
    ├── sweep.py                # Multi-board harvester & track classifier
    ├── scorecard.py            # Funnel conversion metrics generator
    └── gmail_sync.py           # Gmail reply tracker & alert monitor
```

---

## ⚡ Quick Start

### 1. Installation

#### Gemini Antigravity / Gemini CLI:
Copy or mount the plugin inside your workspace:
```bash
cp -r ai-job-hunter /path/to/workspace/.agents/plugins/
```

#### Anthropic Claude Code:
Link or copy into `.claude/`:
```bash
cp -r ai-job-hunter/.claude/* /path/to/workspace/.claude/
```

#### OpenAI Codex:
Point Codex to `CODEX.md` or mount `ai-job-hunter` as workspace root.

---

### 2. Workflow Usage

#### A. Deduplication Check
Verify whether a requisition has already been processed:
```bash
python3 scripts/dedupe.py --check "Company Name" "https://jobs.example.com/posting"
```

#### B. Tailor Bespoke Materials
Generate and compile bespoke single-page LaTeX CV and Cover Letter:
```bash
python3 scripts/latex_builder.py --cv "Prabhavit_CV_TargetCompany.tex"
python3 scripts/latex_builder.py --letter "CoverLetter_TargetCompany.tex"
```

#### C. Autonomous Browser Submission
Submit with automated 8-box IMAP Gmail OTP verification:
```bash
python3 scripts/apply_greenhouse.py \
  --url "https://job-boards.greenhouse.io/example/jobs/12345" \
  --company "Example Company" \
  --role "AI Software Engineer" \
  --cv "Prabhavit_CV_Example.pdf" \
  --letter "CoverLetter_Example.pdf"
```

---

## 📊 Conversion Funnel Scorecard

Generate conversion analytics from `applications.csv`:
```bash
python3 scripts/scorecard.py
```

Output includes:
- Total submissions count
- ATS breakdown (Greenhouse, Lever, Ashby, Personio, Workable, etc.)
- Active interviews and screening metrics
- Rejection rates and ghosted applications

---

## 🔒 Hard Invariants & Constraints

1. **Zero Em-Dashes:** Standard ASCII hyphens (` - `) strictly enforced across all files, code, LaTeX, and markdown.
2. **Transparent Work Authorization:** Italian EU Long-Term Residence Permit (*Permesso di Soggiorno UE per Soggiornanti di Lungo Periodo* - permanent resident, EU Directive 2003/109/EC mobility, zero sponsorship needed in Italy or EU remote/hybrid).
3. **Accurate Contact Facts:** Phone `+39 351 610 7807`, Email `prabhavitg@gmail.com`, Location Venice, Italy (CET).
4. **Exact 10-Field Ledger:** `date,company,role,ats,url,status,confirmation_text,salary_stated,cover_letter_attached,notes`.
5. **Zero AI Attribution:** Absolute prohibition of AI generation disclaimers or Co-Authored-By lines in submitted materials.

---

## 📄 License

Distributed under the [MIT License](LICENSE). Built for high-signal autonomous career execution.
