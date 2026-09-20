#!/usr/bin/env python3
"""Automated Application Dispatcher & Runner for Direct ATS & Web Postings.
Coordinates material discovery, browser verification, and ledger updating.
"""

import csv
import datetime as dt
import os
import re
import sys
import time

def find_workspace_root():
    cur = os.path.abspath(os.getcwd())
    while cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, "applications.csv")) or os.path.exists(os.path.join(cur, "loop")):
            return cur
        cur = os.path.dirname(cur)
    return os.path.abspath(os.getcwd())

ROOT = find_workspace_root()
CONFIRM_DIR = os.path.join(ROOT, "confirmations")
os.makedirs(CONFIRM_DIR, exist_ok=True)

CANDIDATE = {
    "first_name": "Prabhavit",
    "last_name": "Gupta",
    "full_name": "Prabhavit Gupta",
    "email": "prabhavitg@gmail.com",
    "phone": "+39 351 610 7807",
    "location": "Venice, Italy",
    "city": "Venice",
    "country": "Italy",
    "postal_code": "30175",
    "linkedin": "https://www.linkedin.com/in/prabhavit/",
    "github": "https://github.com/prab-gupta",
    "salary_eur": "50000",
    "authorized_italy": "Yes",
    "sponsorship_needed": "No"
}

def clean_slug(s):
    return re.sub(r"[^a-zA-Z0-9]", "", s)

def find_materials(company):
    slug = clean_slug(company)
    cv_candidates = [
        os.path.join(ROOT, f"Prabhavit_CV_{slug}.pdf"),
        os.path.join(ROOT, f"Prabhavit_CV_{slug}FDE.pdf"),
        os.path.join(ROOT, "Prabhavit_CV_EN.pdf"),
        os.path.join(ROOT, "Prabhavit_CV.pdf"),
        os.path.join(ROOT, "Prabhavit_CV_Standard.pdf")
    ]
    cv_pdf = next((c for c in cv_candidates if os.path.exists(c)), None)

    cl_candidates = [
        os.path.join(ROOT, f"CoverLetter_{slug}.pdf"),
        os.path.join(ROOT, f"CoverLetter_{slug}FDE.pdf"),
        os.path.join(ROOT, f"CoverLetter_{slug}.txt")
    ]
    cl_file = next((c for c in cl_candidates if os.path.exists(c)), None)

    return cv_pdf, cl_file

def log_submission(company, role, ats, url, status="SUBMITTED", conf_text="Application submitted", notes=""):
    today = dt.date.today().isoformat()
    csv_file = os.path.join(ROOT, "applications.csv")
    row = [
        today,
        company,
        role,
        ats,
        url,
        status,
        conf_text,
        CANDIDATE["salary_eur"],
        "Yes",
        notes
    ]
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(row)
    print(f"Logged {status} for {company} - {role} to applications.csv")

def main():
    print("AI Job Hunter Application Dispatcher Initialized.")
    print(f"Workspace Root: {ROOT}")
    print(f"Candidate: {CANDIDATE['full_name']} ({CANDIDATE['email']})")

if __name__ == "__main__":
    main()
