#!/usr/bin/env python3
"""Universal Personio Submitter for the AI Job Hunter Plugin.

Usage:
  python3 scripts/apply_personio.py --url "<Personio_URL>" --company "<Company>" --role "<Role>" --cv "<CV_Path>" --letter "<Letter_Path>"
"""

import os, sys, time, datetime as dt, csv, re, argparse
from playwright.sync_api import sync_playwright

def find_workspace_root():
    cur = os.path.abspath(os.getcwd())
    while cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, "applications.csv")):
            return cur
        cur = os.path.dirname(cur)
    return os.path.abspath(os.getcwd())

ROOT = find_workspace_root()
CONFIRM_DIR = os.path.join(ROOT, "confirmations")
os.makedirs(CONFIRM_DIR, exist_ok=True)

def apply_personio(url, company, role, cv_path, letter_path=None, salary="EUR 50,000 / year"):
    print("==========================================")
    print(f"Applying to (Personio): {company} - {role}")
    print(f"URL: {url}")
    print("==========================================")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(2000)
        
        # Click Apply button if present
        apply_btn = page.locator("a:has-text('Auf diese Stelle bewerben'), button:has-text('Auf diese Stelle bewerben'), a:has-text('Apply'), button:has-text('Apply')").first
        if apply_btn.count() > 0:
            apply_btn.click()
            page.wait_for_timeout(2000)
            
        # Fill inputs
        for inp in page.locator("input, textarea").all():
            name = (inp.get_attribute("name") or "").lower()
            id_ = (inp.get_attribute("id") or "").lower()
            comb = f"{name} {id_}"
            
            if "first" in comb or "vorname" in comb:
                inp.fill("Prabhavit")
            elif "last" in comb or "nachname" in comb:
                inp.fill("Gupta")
            elif "email" in comb:
                inp.fill("prabhavitg@gmail.com")
            elif "phone" in comb or "telefon" in comb:
                inp.fill("+39 351 610 7807")
            elif "salary" in comb or "gehalt" in comb:
                inp.fill(salary)
                
        # File uploads
        cv_slot = page.locator("input[type='file'][name*='resume' i], input[type='file'][name*='cv' i], input[type='file']").first
        if cv_slot.count() > 0:
            cv_slot.set_input_files(cv_path)
            page.wait_for_timeout(1000)
            
        if letter_path:
            cl_slot = page.locator("input[type='file'][name*='cover' i], input[type='file'][name*='anschreiben' i]").first
            if cl_slot.count() > 0:
                cl_slot.set_input_files(letter_path)
                page.wait_for_timeout(1000)
                
        # Mandatory GDPR checkbox
        privacy_cb = page.locator("input[type='checkbox']").first
        if privacy_cb.count() > 0 and not privacy_cb.is_checked():
            privacy_cb.check()
            
        page.wait_for_timeout(1500)
        
        submit = page.locator("button[type='submit'], input[type='submit'], button:has-text('Bewerbung abschicken'), button:has-text('Send application')").last
        submit.scroll_into_view_if_needed()
        submit.click()
        page.wait_for_timeout(5000)
        
        today = dt.date.today().isoformat()
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', company)
        confirm_png = os.path.join(CONFIRM_DIR, f"{clean_name}-{today}.png")
        page.screenshot(path=confirm_png, full_page=True)
        
        body_text = page.inner_text("body")
        if any(w in body_text.lower() for w in ["thank you", "erfolgreich", "received", "vielen dank"]):
            row = [
                today, company, role, "Personio", url, "SUBMITTED",
                "Your application has been received.", salary, "yes" if letter_path else "no",
                f"Submitted via Personio automated submitter. Screenshot: {confirm_png}"
            ]
            with open(os.path.join(ROOT, "applications.csv"), "a", newline="", encoding="utf-8") as f_csv:
                csv.writer(f_csv).writerow(row)
            print(f"SUCCESS: Application to {company} submitted on Personio!")
            browser.close()
            return True
            
        browser.close()
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--company", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--cv", required=True)
    parser.add_argument("--letter", required=False)
    args = parser.parse_args()
    apply_personio(args.url, args.company, args.role, args.cv, args.letter)
