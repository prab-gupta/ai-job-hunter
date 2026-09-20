# ATS Quirks & Platform Workarounds

Field mappings, form quirks, anti-bot mechanisms, and automated browser handling across primary ATS platforms.

---

## 1. Greenhouse (`job-boards.greenhouse.io` / `boards.greenhouse.io`)
- **CV / Resume:** File input `#resume` or `input[type="file"][id*="resume"]`.
- **Cover Letter:** File input `#cover_letter` or paste into `textarea#cover_letter_text`.
- **React Custom Dropdowns:** Dropdowns use `react-select`. Options are rendered with IDs starting with `react-select-{field_id}-option-`.
- **8-Box Security Code Automation (Modern Greenhouse):**
  - High-volume job postings trigger human verification splitting an 8-character token across 8 inputs (`#security-input-0` through `#security-input-7`).
  - Automated workflow: Query Gmail via IMAP (`prabhavitg@gmail.com`), extract token from `<h1>([a-zA-Z0-9]{8})</h1>`, fill each single-character box sequentially, and trigger submission.
- **Verification:** Successful submission displays *"Your application has been received"* or *"Thank you for your interest"*.

---

## 2. Lever (`jobs.lever.co`)
- **CV / Resume:** Drag-and-drop or file input at top (`input[type="file"]`).
- **Location:** Plain text input; does not require autocomplete dropdown selection.
- **Additional Information:** Textarea for cover letter or freeform notes.
- **Quirks:** Fast single-page submit; confirmation displays *"Application submitted!"* with a checkmark.

---

## 3. Ashby (`jobs.ashbyhq.com`)
- **Location Field:** Must type location (*"Venice, Italy"* or *"Remote"*) AND click the matching autocomplete dropdown item from the rendered list.
- **Keystroke Events:** Requires real keystroke input simulation; direct DOM value assignment without input/change event dispatch will cause form submission errors.
- **Cloudflare Turnstile:** Staged for quick user click if challenge is active.
- **Confirmation:** Displays *"Application Received"*.

---

## 4. Workable (`apply.workable.com`)
- **Autofill Side Effect:** Uploading a CV causes Workable to auto-parse and overwrite name, phone, and address fields. Always inspect and refill phone (`+39 351 610 7807`) and location (`Venice, Italy`) after uploading the resume PDF.
- **Direct Apply URL:** `https://apply.workable.com/<company>/j/<id>/apply/`.
- **Quirks:** Multi-step wizard with final review before submission.

---

## 5. Personio (`<company>.jobs.personio.de`)
- **File Slots:** Distinct upload containers for `Lebenslauf / CV` and `Anschreiben / Cover Letter`.
- **Language Switch:** If displayed in German, look for language toggle (DE/EN) or fill English answers.
- **Mandatory Consent:** Check mandatory GDPR data processing consent box.

---

## 6. Trakstar Hire (`<company>.hire.trakstar.com`)
- **Direct Apply Endpoint:** Trakstar job pages with *"Apply with Indeed"* button lead to IP blocks. Always navigate directly to `?apply=true` or `#apply` to access the native form fields cleanly without CAPTCHA.
- **Confirmation:** Displays *"Your application has been submitted successfully!"*.

---

## 7. Teamtailor (`<company>.teamtailor.com`)
- **Quick Apply Modal:** Many Teamtailor portals open an overlay modal.
- **Quirks:** CV upload autofills fields; ensure phone number retains the international `+39` prefix.
- **Confirmation:** Displays *"Thanks for applying. We have received your application"*.

---

## 8. SmartRecruiters (`jobs.smartrecruiters.com`)
- **One-Click Apply:** Standard form with CV and Cover Letter upload slots.
- **DataDome Protection:** If DataDome slider appears, hand back to user or solve via persistent Chrome profile.
