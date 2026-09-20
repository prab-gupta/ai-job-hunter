# /sweep - Harvest Fresh Job Postings

Harvest, filter, and deduplicate fresh software, AI, FDE, and solutions engineering leads across multiple job aggregators.

## Steps
1. Run multi-aggregator harvest script:
   ```bash
   python3 scripts/sweep.py
   ```
2. Filter leads against target tracks (Track A: AI/Automation, Track B: FDE/Solutions, Track C: Full-Stack/Product).
3. Deduplicate against `applications.csv` and staging ledgers.
4. Output qualified leads ready for bespoke tailoring.
