---
name: cv-tailor
description: Generate and compile bespoke, single-page LaTeX CVs and cover letters tailored specifically to job requisitions.
---

# CV & Cover Letter Tailoring Skill

This skill creates bespoke, highly targeted application materials in LaTeX, compiling them to PDF using `tectonic`.

## 1. Materials Policy

- **LinkedIn Easy Apply:** Use standard high-signal CV (`templates/Prabhavit_CV_Base.pdf`).
- **All Direct Portals / ATS Applications:** A **custom-tailored CV and Cover Letter are strictly mandatory**.
- **Hard Constraints:**
  - Zero em-dashes (` - ` standard only).
  - Max 1 page for CVs (or 2 pages if multi-role senior track requires, strictly verified via `pdfinfo`).
  - Cover letter length: 250 - 320 words, precisely targeted to the company problem domain.
  - Transparent Italian EU Long-Term Residence Permit (*Permesso di Soggiorno UE per Soggiornanti di Lungo Periodo*).
  - No AI attribution lines or disclaimers.

---

## 2. CV Tailoring Workflow

1. Read the target Job Description (JD) and extract key requirements, tech stack, and pain points.
2. Select the base LaTeX template from `templates/Prabhavit_CV_Base.tex`.
3. Select lead and secondary roles from `reference/MASTER_EXPERIENCE.md` matching the JD:
   - **CV Parsing / Document AI / HR Tech:** Lead with UltraStrategy, pair with FlowSpace AI listing bot.
   - **AI-Assisted Dev / Agency / Client Delivery:** Lead with Urlink, pair with UltraStrategy or FlowSpace.
   - **API Integrations / Search Automations:** Lead with Get2Germany, pair with FlowSpace.
   - **Marketplace / Production Agents / GTM:** Lead with FlowSpace, pair with Urlink or Get2Germany.
4. Modify **only** the `HEADLINE`, `SUMMARY`, and `SKILLS` sections of the template. Experience bullet points must remain factually grounded in `MASTER_EXPERIENCE.md`.
5. Compile to PDF:
   ```bash
   python3 scripts/latex_builder.py --cv "Prabhavit_CV_<Company>.tex"
   ```
6. Verify page count using `pdfinfo Prabhavit_CV_<Company>.pdf | grep Pages`.

---

## 3. Cover Letter Drafting Workflow

1. Create `CoverLetter_<Company>.tex` using `templates/CoverLetter_Base.tex`.
2. Cover Letter Structure:
   - **Opening:** Direct statement of enthusiasm for the exact position and team.
   - **Core Proof 1:** Concrete technical achievement matching their core stack (e.g. LLM extraction, agent workflows, API integrations).
   - **Core Proof 2:** Client delivery, end-to-end execution, or system migration impact.
   - **Logistics & Auth:** Permanent resident holding an Italian EU Long-Term Residence Permit (*Permesso di Soggiorno UE per Soggiornanti di Lungo Periodo*), CET timezone, immediate availability.
   - **Closing:** Professional sign-off.
3. Compile via `python3 scripts/latex_builder.py --letter "CoverLetter_<Company>.tex"`.
4. Also save plain text version `CoverLetter_<Company>.txt` for direct form paste fields.
