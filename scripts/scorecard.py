#!/usr/bin/env python3
"""Funnel Analytics and Scorecard Generator for the AI Job Hunter Plugin.
Reconciles applications.csv with Gmail threads and generates SCORECARD.md.
"""

import collections
import csv
import datetime
import json
import os
import re
import sys

def find_workspace_root():
    cur = os.path.abspath(os.getcwd())
    while cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, "applications.csv")) or os.path.exists(os.path.join(cur, "loop")):
            return cur
        cur = os.path.dirname(cur)
    return os.path.abspath(os.getcwd())

ROOT = find_workspace_root()
THREADS_PATH = os.path.join(ROOT, "loop", "gmail_threads.jsonl")
CSV_PATH = os.path.join(ROOT, "applications.csv")
OUT_PATH = os.path.join(ROOT, "loop", "SCORECARD.md")

def desh(s):
    return (s or "").replace(" - ", "-").replace("–", "-")

LEGAL_SUFFIXES = (
    "inc", "llc", "ltd", "gmbh", "ag", "corp", "corporation", "spa", "bv",
    "srl", "plc", "co", "sa", "group", "sro", "oy", "ab", "as", "kft"
)

def normalize(s):
    s = (s or "").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    words = s.split()
    words = [w for w in words if w not in LEGAL_SUFFIXES]
    return " ".join(words).strip()

def sub_match(a, b):
    if len(a) < 4 or len(b) < 4:
        return a == b and a != ""
    return a in b or b in a

def generate_scorecard():
    threads = []
    if os.path.exists(THREADS_PATH):
        with open(THREADS_PATH, "r", encoding="utf-8") as f:
            for l in f:
                if l.strip():
                    try:
                        t = json.loads(l)
                        t["subject"] = desh(t.get("subject"))
                        t["company"] = desh(t.get("company"))
                        t["snippet"] = desh(t.get("snippet"))
                        threads.append(t)
                    except Exception:
                        pass

    csv_rows = []
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline="", encoding="utf-8", errors="replace") as f:
            r = csv.reader(f)
            header = next(r, None)
            for row in r:
                if len(row) >= 6:
                    company = row[1]
                    role = row[2]
                    ats = row[3]
                    status = row[5]
                    csv_rows.append((normalize(company), role, ats, status, False, row))
                elif row:
                    full = normalize(" ".join(row))
                    role = row[2] if len(row) > 2 else ""
                    ats = row[3] if len(row) > 3 else ""
                    status = row[5] if len(row) > 5 else ""
                    csv_rows.append((full, role, ats, status, True, row))

    def match_thread_company(company):
        tc = normalize(company)
        if len(tc) < 4:
            return None
        for norm_c, role, ats, status, is_full, row in csv_rows:
            if is_full:
                if tc in norm_c:
                    return role, ats, status, row
            else:
                if sub_match(tc, norm_c):
                    return role, ats, status, row
        return None

    for t in threads:
        m = match_thread_company(t.get("company", ""))
        if m:
            t["matched_role"] = m[0]
            t["matched_ats"] = m[1]
            t["matched_status"] = m[2]
            t["matched"] = True
        else:
            t["matched_role"] = None
            t["matched_ats"] = None
            t["matched_status"] = None
            t["matched"] = False

    total_submitted = len([r for r in csv_rows if len(r) > 3 and "SUBMITTED" in r[3].upper()])
    by_status = collections.Counter(r[3].upper() for r in csv_rows if len(r) > 3)
    by_class = collections.Counter(t.get("cls") for t in threads)

    scorecard_lines = [
        "# Job Application Scorecard & Funnel Analytics",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Funnel Overview",
        f"- **Total CSV Applications Recorded:** {len(csv_rows)}",
        f"- **Confirmed SUBMITTED Applications:** {total_submitted}",
        f"- **Gmail Threads Monitored:** {len(threads)}",
        f"- **Rejection Notices Received:** {by_class.get('REJECT', 0)}",
        f"- **Interviews / Positive Responses:** {by_class.get('INTERVIEW', 0)}",
        "",
        "## Applications by Status",
        "| Status | Count |",
        "|---|---|"
    ]

    for st, count in by_status.most_common():
        scorecard_lines.append(f"| {st} | {count} |")

    scorecard_lines.extend([
        "",
        "## Recent Gmail Responses",
        "| Company | Type | Subject | Date |",
        "|---|---|---|---|"
    ])

    for t in threads[-15:]:
        scorecard_lines.append(f"| {t.get('company', 'Unknown')} | {t.get('cls', 'OTHER')} | {t.get('subject', '')[:50]} | {t.get('date', '')[:10]} |")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(scorecard_lines) + "\n")

    print(f"Scorecard generated at {OUT_PATH}: {len(csv_rows)} CSV rows, {len(threads)} Gmail threads.")

if __name__ == "__main__":
    generate_scorecard()
