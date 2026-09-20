#!/usr/bin/env python3
"""Universal Greenhouse Submitter with Automated 8-Box IMAP Gmail OTP Resolution.
Part of the AI Job Hunter Plugin.

Usage:
  python3 scripts/apply_greenhouse.py --url "<Greenhouse_URL>" --company "<Company>" --role "<Role>" --cv "<CV_Path>" --letter "<Letter_Path>"
"""

import os, sys, time, datetime as dt, csv, imaplib, email, re, argparse
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

def get_greenhouse_otp(timeout_sec=90):
    user = "prabhavitg@gmail.com"
    pwd = "xeoa zwqw caqg uqza"
    start = time.time()
    print("Polling Gmail for Greenhouse verification code...")
    while time.time() - start < timeout_sec:
        try:
            m = imaplib.IMAP4_SSL("imap.gmail.com")
            m.login(user, pwd)
            m.select("inbox")
            status, msgs = m.search(None, '(FROM "greenhouse")')
            if status == "OK" and msgs[0]:
                msg_ids = msgs[0].split()
                latest_id = msg_ids[-1]
                res, data = m.fetch(latest_id, "(RFC822)")
                msg = email.message_from_bytes(data[0][1])
                body = ""
                for part in msg.walk():
                    if part.get_content_type() in ["text/plain", "text/html"]:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode("utf-8", errors="ignore")
                
                h1_match = re.search(r"<h1>([a-zA-Z0-9]{8})</h1>", body)
                if h1_match:
                    code = h1_match.group(1)
                    print(f"Retrieved 8-char security code: {code}")
                    m.logout()
                    return code
                
                m8 = re.search(r"\b([a-zA-Z0-9]{8})\b", body)
                if m8:
                    code = m8.group(1)
                    if not code.startswith("http") and not code.startswith("0000"):
                        print(f"Retrieved 8-char candidate code: {code}")
                        m.logout()
                        return code
            m.logout()
        except Exception as e:
            print("IMAP check notice:", e)
        time.sleep(3)
    return None

def select_gh_react(page, field_id, target_text=None, index=0, wait_ms=300):
    container = page.locator(f'label[for="{field_id}"]').locator("..")
    ctrl = container.locator(".select__control")
    if ctrl.count() == 0:
        return False
    ctrl.scroll_into_view_if_needed()
    ctrl.click()
    page.wait_for_timeout(wait_ms)
    
    opts = page.locator(f'div[id^="react-select-{field_id}-option-"]').all()
    if not opts:
        page.wait_for_timeout(400)
        opts = page.locator(f'div[id^="react-select-{field_id}-option-"]').all()
        
    if target_text:
        for opt in opts:
            txt = opt.text_content().strip()
            if target_text.lower() in txt.lower():
                opt.click()
                print(f"  Selected {field_id} -> {txt}")
                page.wait_for_timeout(200)
                return True
    if opts:
        txt = opts[index].text_content().strip()
        opts[index].click()
        print(f"  Selected {field_id} (index {index}) -> {txt}")
        page.wait_for_timeout(200)
        return True
    else:
        page.keyboard.press("Escape")
        return False

def apply_greenhouse(url, company, role, cv_path, letter_path=None, salary="EUR 50,000 / year"):
    print("==========================================")
    print(f"Applying to: {company} - {role}")
    print(f"URL: {url}")
    print(f"CV: {cv_path}")
    print(f"Cover Letter: {letter_path}")
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
        
        # Standard contact fields
        if page.locator("#first_name").count() > 0:
            page.locator("#first_name").fill("Prabhavit")
        if page.locator("#last_name").count() > 0:
            page.locator("#last_name").fill("Gupta")
        if page.locator("#preferred_name").count() > 0:
            page.locator("#preferred_name").fill("Prabhavit")
        if page.locator("#email").count() > 0:
            page.locator("#email").fill("prabhavitg@gmail.com")
        if page.locator("#phone").count() > 0:
            page.locator("#phone").fill("+393516107807")
            
        # File uploads
        if page.locator("#resume").count() > 0:
            page.locator("#resume").set_input_files(cv_path)
            page.wait_for_timeout(500)
        if letter_path and page.locator("#cover_letter").count() > 0:
            page.locator("#cover_letter").set_input_files(letter_path)
            page.wait_for_timeout(500)
            
        # Education
        if page.locator("#school--0").count() > 0:
            select_gh_react(page, "school--0", index=0)
        if page.locator("#degree--0").count() > 0:
            select_gh_react(page, "degree--0", target_text="Bachelor's Degree")
        if page.locator("#discipline--0").count() > 0:
            select_gh_react(page, "discipline--0", target_text="Economics", wait_ms=600)
            
        # Auto-fill common inputs
        for inp in page.locator("input[type='text'], textarea").all():
            label = page.locator(f"label[for='{inp.get_attribute('id')}']").text_content() if inp.get_attribute('id') else ""
            lbl = label.lower()
            if "linkedin" in lbl:
                inp.fill("https://www.linkedin.com/in/prabhavit/")
            elif "github" in lbl or "website" in lbl or "portfolio" in lbl:
                inp.fill("https://github.com/prab-gupta")
            elif "salary" in lbl or "compensation" in lbl:
                inp.fill(salary)
            elif "notice" in lbl or "start date" in lbl:
                inp.fill("Immediately (2 weeks notice max)")
                
        page.wait_for_timeout(1500)
        
        # Click submit button
        submit_btn = page.locator("button[type='submit'], button#submit_app, button:has-text('Submit application')").last
        submit_btn.scroll_into_view_if_needed()
        submit_btn.click()
        page.wait_for_timeout(5000)
        
        # Check for 8-box OTP code
        if page.locator("#security-input-0").count() > 0 or page.locator("input[id^='security-input-']").count() > 0:
            print("Security verification code required. Polling Gmail...")
            code = get_greenhouse_otp()
            if code:
                for i, ch in enumerate(code):
                    b = page.locator(f"#security-input-{i}")
                    if b.count() > 0:
                        b.fill(ch)
                        page.wait_for_timeout(100)
                page.wait_for_timeout(1000)
                submit_btn = page.locator("button[type='submit'], button#submit_app, button:has-text('Submit application')").last
                submit_btn.click()
                page.wait_for_timeout(8000)
                
        today = dt.date.today().isoformat()
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', company)
        confirm_png = os.path.join(CONFIRM_DIR, f"{clean_name}-{today}.png")
        confirm_txt = os.path.join(CONFIRM_DIR, f"{clean_name}-{today}.txt")
        page.screenshot(path=confirm_png, full_page=True)
        
        body_text = page.inner_text("body")
        if any(w in body_text.lower() for w in ["thank you", "thanks", "received", "submitted"]):
            with open(confirm_txt, "w") as f:
                f.write(f"Company: {company}\nRole: {role}\nURL: {url}\nDate: {today}\nStatus: SUBMITTED\n")
            row = [
                today, company, role, "Greenhouse", url, "SUBMITTED",
                "Your application has been received.", salary, "yes" if letter_path else "no",
                f"Submitted via automated Greenhouse flow with OTP verification. Screenshot: {confirm_png}"
            ]
            with open(os.path.join(ROOT, "applications.csv"), "a", newline="", encoding="utf-8") as f_csv:
                csv.writer(f_csv).writerow(row)
            print(f"SUCCESS: Application to {company} submitted and logged!")
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
    apply_greenhouse(args.url, args.company, args.role, args.cv, args.letter)
