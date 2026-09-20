# /tailor - Tailor Bespoke Application Materials

Generate and compile single-page LaTeX CV and Cover Letter for a target job requisition.

## Steps
1. Parse target job posting requirements, stack, and domain.
2. Load candidate details from `reference/candidate_profile.json` and `reference/MASTER_EXPERIENCE.md`.
3. Weave candidate experiences (FlowSpace.co, UltraStrategy, Clubee, Get2Germany, Urlink, and `llm-doc-parser`).
4. Generate `Prabhavit_CV_<Company>.tex` and `CoverLetter_<Company>.tex`.
5. Compile and verify with `scripts/latex_builder.py`:
   ```bash
   python3 scripts/latex_builder.py --cv "Prabhavit_CV_<Company>.tex"
   python3 scripts/latex_builder.py --letter "CoverLetter_<Company>.tex"
   ```
6. Ensure zero em-dashes and exact 1-page constraints.
