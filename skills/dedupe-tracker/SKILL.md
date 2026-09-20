---
name: dedupe-tracker
description: Deduplicate job postings against historical ledgers, validate 10-field CSV schema, and generate conversion scorecards.
---

# Deduplication & Tracker Skill

This skill enforces corpus-wide deduplication and data integrity across application ledgers (`applications.csv`, `queue.csv`, `corpus.json`).

## 1. Multi-Tier Deduplication Engine

The deduplication engine scans across URLs, ATS IDs, normalized company names, and known aliases:

1. **Exact & Normalized URL Match:** Strips UTM tags, marketing queries, and hash fragments. Retains requisition IDs (`jobId`, `gh_jid`, `id`, `req`).
2. **Numeric ATS ID Match:** Extracts 7+ digit job IDs to catch cross-posted URLs for the exact same opening.
3. **Company Name Normalization:** Strips legal entity suffixes (`Inc`, `Ltd`, `GmbH`, `S.r.l.`, `S.p.A.`, `B.V.`, `AG`, `Corp`, `Technologies`).
4. **Brand Alias Resolution:** Maps subsidiary brand names to parent ATS domains (e.g. `MAU / AI-LAB` -> `Leadtech`, `Transcendent Group` -> `Advisense`).

---

## 2. CLI Deduplication Commands

```bash
# Check if a company or job URL has already been processed
python3 scripts/dedupe.py --check "Cohere" "https://jobs.ashbyhq.com/cohere/2d256112"
# Output: HIT URL or NEW

# Rebuild the deduplication cache (corpus.json) across all CSVs and workbooks
python3 scripts/dedupe.py --rebuild
```

---

## 3. CSV Ledger Schema & Validation

All application records in `applications.csv` must follow the strict 10-field CSV schema:

| Field Index | Field Name | Description / Valid Values |
|---|---|---|
| 0 | `date` | Submission date in `YYYY-MM-DD` format |
| 1 | `company` | Exact company name |
| 2 | `role` | Exact job title |
| 3 | `ats` | ATS platform (`Greenhouse`, `Lever`, `Ashby`, `LinkedIn Easy Apply`, etc.) |
| 4 | `url` | Clean requisition apply URL |
| 5 | `status` | Standard status (`SUBMITTED`, `TO APPLY`, `NEEDS YOU`, `BLOCKED`, `REJECTED`, `INTERVIEW`) |
| 6 | `confirmation_text` | Text snippet from the on-screen submission receipt |
| 7 | `salary_stated` | Disclosed or stated salary band |
| 8 | `cover_letter_attached` | `Yes` or `No` |
| 9 | `notes` | Confirmation screenshot path or deduplication receipt |

---

## 4. Scorecard & Reconciliation Reporting

Run `python3 scripts/scorecard.py` to reconcile `applications.csv` against incoming emails in `gmail_threads.jsonl`, generating a complete funnel report in `SCORECARD.md`:
- Total submissions count
- Interview invite rates
- Platform rejection distributions
- Missing CSV entries for detected email threads
