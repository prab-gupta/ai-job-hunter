# /loop - Continuous Application Loop

Orchestrate the continuous autonomous job application loop with checkpointing.

## Steps
1. Read `loop/STATE.md` and `AGENTS.md` fresh.
2. Execute ONE unit of work per tick:
   - Priority 1: If ready target exists in queue, tailor materials, run browser submitter, and record confirmation.
   - Priority 2: Harvest fresh postings across platforms.
   - Priority 3: Sync Gmail replies and interview invitations.
3. Update and rewrite `loop/STATE.md` (strictly <= 60 lines).
