# /apply - Submit Job Application

Submit tailored application via automated browser or native submitter with verification.

## Steps
1. Run deduplication check:
   ```bash
   python3 scripts/dedupe.py --check "<Company>" "<Job_URL>"
   ```
2. If `NEW`, execute the appropriate submitter:
   - Greenhouse (with automated 8-box OTP): `python3 scripts/apply_greenhouse.py --url "<URL>" --company "<Company>" --role "<Role>" --cv "<CV>" --letter "<Letter>"`
   - Ashby: `python3 scripts/apply_ashby.py --url "<URL>" --company "<Company>" --role "<Role>" --cv "<CV>" --letter "<Letter>"`
   - Personio: `python3 scripts/apply_personio.py --url "<URL>" --company "<Company>" --role "<Role>" --cv "<CV>" --letter "<Letter>"`
   - Workable: `python3 scripts/apply_workable.py --url "<URL>" --company "<Company>" --role "<Role>" --cv "<CV>" --letter "<Letter>"`
3. Verify on-screen confirmation and save screenshot into `confirmations/`.
4. Append 10-field row to `applications.csv`.
