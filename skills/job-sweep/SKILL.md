---
name: job-sweep
description: Harvest and filter fresh tech, AI, FDE, and software engineer job postings across LinkedIn, Greenhouse, Lever, Ashby, FreeHire, and Nordic boards.
---

# Job Sweep & Harvesting Skill

This skill queries public job aggregators, ATS board APIs, and search engines to discover high-match opportunities, filtering them through the candidate's qualification criteria.

## 1. Supported Portals & Query Strategies

1. **LinkedIn API & Web Search:**
   - Queries: `Forward Deployed Engineer`, `AI Engineer`, `Solutions Engineer AI`, `Automation Engineer`, `Product Engineer AI`, `GTM Engineer`.
   - Geo targets: Italy (`geoId: 103350119`), European Union (`geoId: 91000000`), Worldwide Remote.
   - Time window: `f_TPR=r86400` (past 24h) on weekdays, `f_TPR=r604800` (past week) on weekends.
2. **Direct ATS Sweepers:**
   - Greenhouse (`job-boards.greenhouse.io/<org>`)
   - Lever (`jobs.lever.co/<org>`)
   - Ashby (`jobs.ashbyhq.com/<org>`)
   - Workable (`apply.workable.com/<org>`)
   - Personio (`<org>.jobs.personio.de`)
   - Recruitee (`<org>.recruitee.com`)
   - Teamtailor (`<org>.teamtailor.com`)
3. **Aggregator APIs:**
   - FreeHire (`freehire-search`)
   - Nordic Job Portals (`jobnet-search`, `jobindex-search`, `jobdanmark-search`, `jobbank-search`)

---

## 2. Gating & Scoring Pipeline

Every harvested candidate lead must pass through the `sweep.py` gating engine:

1. **Deduplication Check:** Query `scripts/dedupe.py` to discard already applied URLs and companies.
2. **Title Exclusions:** Drop any posting matching `senior|staff|principal|lead|head|director|vp|chief` unless specifically flagged as candidate-compatible.
3. **Language Gate:** Discard postings requiring fluent non-English languages (German, French, Polish, Dutch) unless located in Italy (where Italian conversational B1-B2 applies).
4. **Experience Gate:** Ensure the role requires <=3 years of professional experience.
5. **Stack Relevance:** Check for match across TypeScript, Next.js, Python, Node.js, LLMs, AI agents, APIs, or integrations.

---

## 3. Usage & CLI Invocations

```bash
# Run multi-aggregator sweep and output to queue
python3 scripts/sweep.py --output loop/fresh_harvest_leads.json

# Sweep specific track (e.g. Forward Deployed Engineer)
python3 scripts/sweep.py --track fde --geo eu --output loop/fde_eu_leads.json
```
