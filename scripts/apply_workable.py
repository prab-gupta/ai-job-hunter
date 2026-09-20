#!/usr/bin/env python3
"""Universal Workable Submitter for the AI Job Hunter Plugin.

Usage:
  python3 scripts/apply_workable.py --url "<Workable_URL>" --company "<Company>" --role "<Role>" --cv "<CV_Path>" --letter "<Letter_Path>"
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

def apply_workable(url, company, role, cv_path, letter_path=None, salary="EUR 50,000 / year"):
    print("==========================================")
    print(f"Applying to (Workable): {company} - {role}")
    print(f"URL: {url}")
    print("==========================================")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()
        
        # Ensure direct apply URL
        apply_url = url if "/apply" in url else url.rstrip("/") + "/apply"
        page.goto(apply_url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(2000)
        
        # Upload CV first (to absorb autofill overwrite)
        cv_input = page.locator("input[type='file']").first
        if cv_input.count() > 0:
            cv_input.set_input_files(cv_path)
            page.wait_for_timeout(2500)
            
        # Re-enforce accurate contact details after CV parse
        if page.locator("input[name*='firstname' i], input[id*='firstname' i]").count() > 0:
            page.locator("input[name*='firstname' i], input[id*='firstname' i]").first.fill("Prabhavit")
        if page.locator("input[name*='lastname' i], input[id*='lastname' i]").count() > 0:
            page.locator("input[name*='lastname' i], input[id*='lastname' i]").first.fill("Gupta")
        if page.locator("input[name*='email' i], input[type='email']").count() > 0:
            page.locator("input[name*='email' i], input[type='email']").first.fill("prabhavitg@gmail.com")
        if page.locator("input[name*='phone' i], input[type='tel']").count() > 0:
            page.locator("input[name*='phone' i], input[type='tel']").first.fill("+39 351 610 7807")
            
        if letter_path and page.locator("textarea[name*='cover' i], textarea[id*='cover' i]").count() > 0:
            with open(letter_path, "r", errors="ignore") as f:
                page.locator("textarea[name*='cover' i], textarea[id*='cover' i]").first.fill(f.read())
                
        page.wait_for_timeout(1500)
        
        submit_btn = page.locator("button[type='submit'], button:has-text('Submit Application')").last
        submit_btn.scroll_into_view_if_needed()
        submit_btn.click()
        page.wait_for_timeout(5000)
        
        today = dt.date.today().isoformat()
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', company)
        confirm_png = os.path.join(CONFIRM_DIR, f"{clean_name}-{today}.png")
        page.screenshot(path=confirm_png, full_page=True)
        
        body_text = page.inner_text("body")
        if any(w in body_text.lower() for w in ["thank you", "received", "submitted"]):
            row = [
                today, company, role, "Workable", url, "SUBMITTED",
                "Application submitted successfully.", salary, "yes" if letter_path else "no",
                f"Submitted via Workable automated submitter. Screenshot: {confirm_png}"
            ]
            with open(os.path.join(ROOT, "applications.csv"), "a", newline="", encoding="utf-8") as f_csv:
                csv.writer(f_csv).writerow(row)
            print(f"SUCCESS: Application to {company} submitted on Workable!")
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
    apply_workable(args.url, args.company, args.role, args.cv, args.letter)
