---
description: Enforce exact 10-field CSV schema and deduplication ledger integrity for applications.csv.
trigger: always_on
---

# Ledger Integrity & Deduplication Rule

## Canonical CSV Schema
Every application record in `applications.csv` must strictly conform to the 10-field schema:
`date,company,role,ats,url,status,confirmation_text,salary_stated,cover_letter_attached,notes`

## Field Definitions
1. `date`: ISO format (`YYYY-MM-DD`).
2. `company`: Canonical company name.
3. `role`: Job title as stated on requisition.
4. `ats`: Platform identifier (e.g., `Greenhouse`, `Lever`, `Ashby`, `Workable`, `Personio`, `Teamtailor`, `Trakstar`, `Email`, `LinkedIn Easy Apply`).
5. `url`: Direct canonical job URL.
6. `status`: Standard status vocabulary (`SUBMITTED`, `TO APPLY`, `NEEDS YOU`, `BLOCKED`, `DROPPED`, `CLOSED`, `DEAD`, `SKIP - <reason>`, `REPLIED`, `INTERVIEW`, `REJECTED`).
7. `confirmation_text`: Exact text extracted from on-screen confirmation banner or submission response.
8. `salary_stated`: Salary range provided on application (e.g. `EUR 50,000 / year`).
9. `cover_letter_attached`: `yes (<filename>)` or `no`.
10. `notes`: Context, stack alignment, location, and path to confirmation screenshot.

## Deduplication Rule
Before any action is taken on a job posting:
```bash
python3 scripts/dedupe.py --check "<Company>" "<Job_URL>"
```
If output starts with `HIT`, skip immediately.
