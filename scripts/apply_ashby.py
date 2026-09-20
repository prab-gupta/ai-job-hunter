#!/usr/bin/env python3
"""Universal Ashby Submitter for the AI Job Hunter Plugin.

Usage:
  python3 scripts/apply_ashby.py --url "<Ashby_URL>" --company "<Company>" --role "<Role>" --cv "<CV_Path>" --letter "<Letter_Path>"
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

def apply_ashby(url, company, role, cv_path, letter_path=None, salary="EUR 50,000 / year"):
    print("==========================================")
    print(f"Applying to (Ashby): {company} - {role}")
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
        
        # Fill standard inputs
        for inp in page.locator("input, textarea").all():
            name = (inp.get_attribute("name") or "").lower()
            id_ = (inp.get_attribute("id") or "").lower()
            label = page.locator(f"label[for='{inp.get_attribute('id')}']").text_content().lower() if inp.get_attribute('id') else ""
            comb = f"{name} {id_} {label}"
            
            if "first" in comb and "name" in comb:
                inp.fill("Prabhavit")
            elif "last" in comb and "name" in comb:
                inp.fill("Gupta")
            elif "name" in comb and "full" in comb or comb.strip() == "name":
                inp.fill("Prabhavit Gupta")
            elif "email" in comb:
                inp.fill("prabhavitg@gmail.com")
            elif "phone" in comb:
                inp.fill("+39 351 610 7807")
            elif "linkedin" in comb:
                inp.fill("https://www.linkedin.com/in/prabhavit/")
            elif "github" in comb or "website" in comb:
                inp.fill("https://github.com/prab-gupta")
            elif "salary" in comb or "compensation" in comb:
                inp.fill(salary)
                
        # Handle Ashby Location input (type and select dropdown)
        loc_inp = page.locator("input[name*='location' i], input[id*='location' i], input[placeholder*='location' i]").first
        if loc_inp.count() > 0:
            loc_inp.click()
            loc_inp.fill("Venice, Italy")
            page.wait_for_timeout(500)
            dropdown_opt = page.locator("div[class*='option' i], li[role='option'], div[role='option']").first
            if dropdown_opt.count() > 0:
                dropdown_opt.click()
                
        # File uploads
        cv_input = page.locator("input[type='file']").first
        if cv_input.count() > 0:
            cv_input.set_input_files(cv_path)
            page.wait_for_timeout(1000)
            
        if letter_path and page.locator("input[type='file']").count() > 1:
            page.locator("input[type='file']").nth(1).set_input_files(letter_path)
            page.wait_for_timeout(1000)
            
        page.wait_for_timeout(1500)
        
        # Check for Turnstile
        if page.locator("iframe[src*='challenges.cloudflare.com']").count() > 0:
            print("Turnstile challenge detected; staging screenshot for confirmation.")
            
        submit_btn = page.locator("button[type='submit'], button:has-text('Submit Application'), button:has-text('Apply')").last
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
                today, company, role, "Ashby", url, "SUBMITTED",
                "Your application was successfully submitted.", salary, "yes" if letter_path else "no",
                f"Submitted via Ashby automated submitter. Screenshot: {confirm_png}"
            ]
            with open(os.path.join(ROOT, "applications.csv"), "a", newline="", encoding="utf-8") as f_csv:
                csv.writer(f_csv).writerow(row)
            print(f"SUCCESS: Application to {company} submitted on Ashby!")
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
    apply_ashby(args.url, args.company, args.role, args.cv, args.letter)
