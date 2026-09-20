#!/usr/bin/env python3
"""Gmail Thread Sync and Recruiter Response Triage Tool for the AI Job Hunter Plugin.
Connects via IMAP, pulls recruiter responses, categorizes updates (INTERVIEW, REJECT, ACK),
and writes to loop/gmail_threads.jsonl.
"""

import datetime
import email
from email.header import decode_header
import imaplib
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
OUT_FILE = os.path.join(ROOT, "loop", "gmail_threads.jsonl")

USERNAME = os.environ.get("GMAIL_USER", "prabhavitg@gmail.com")
PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "xeoa zwqw caqg uqza")

def decode_mime(header_val):
    if not header_val:
        return ""
    decoded_parts = []
    for part, enc in decode_header(header_val):
        if isinstance(part, bytes):
            try:
                decoded_parts.append(part.decode(enc or "utf-8", errors="replace"))
            except Exception:
                decoded_parts.append(part.decode("utf-8", errors="replace"))
        else:
            decoded_parts.append(str(part))
    return "".join(decoded_parts)

def classify_email(subject, sender, snippet):
    combined = f"{subject} {sender} {snippet}".lower()
    if re.search(r"\b(interview|schedule|screening|phone screen|chat with|speaking with|next round|invitation)\b", combined):
        return "INTERVIEW"
    if re.search(r"\b(unfortunately|not moving forward|other candidates|pursuing other|not selected|regret to inform|decided not to)\b", combined):
        return "REJECT"
    if re.search(r"\b(received your application|application confirmed|thank you for applying|we received|application acknowledged)\b", combined):
        return "ACK"
    return "UPDATE"

def extract_company(sender, subject):
    m = re.search(r"@([a-zA-Z0-9.-]+)", sender)
    domain = m.group(1).lower() if m else ""
    for ats in ["greenhouse.io", "lever.co", "ashbyhq.com", "workable.com", "personio.de", "recruitee.com", "smartrecruiters.com"]:
        if ats in domain:
            domain = domain.replace(ats, "").strip(".")
    m_subj = re.search(r"(?:at|with|from)\s+([A-Za-z0-9\s]+?)(?:\s+[-– - |:]|$)", subject, re.I)
    if m_subj:
        return m_subj.group(1).strip()
    return domain.split(".")[0].capitalize() if domain else "Unknown"

def sync_gmail(days=14):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(USERNAME, PASSWORD)
        mail.select("inbox")

        date_since = (datetime.date.today() - datetime.timedelta(days=days)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{date_since}")')

        if status != "OK":
            print("Failed to query Gmail.", file=sys.stderr)
            return []

        email_ids = messages[0].split()
        threads = []

        for e_id in email_ids[-100:]:
            res, msg_data = mail.fetch(e_id, "(RFC822.SIZE BODY[HEADER.FIELDS (SUBJECT FROM DATE MESSAGE-ID)])")
            if res != "OK":
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_mime(msg.get("Subject", ""))
                    from_ = decode_mime(msg.get("From", ""))
                    date_ = msg.get("Date", "")
                    msg_id = msg.get("Message-ID", "")

                    subj_low = subject.lower()
                    from_low = from_.lower()

                    keywords = ["application", "interview", "role", "position", "candidate", "status", "unfortunately", "moving forward"]
                    ats_keywords = ["greenhouse", "lever", "ashby", "workable", "personio", "recruitee", "teamtailor", "workday", "smartrecruiters"]

                    if any(k in subj_low for k in keywords) or any(a in from_low for a in ats_keywords):
                        cls = classify_email(subject, from_, "")
                        co = extract_company(from_, subject)
                        threads.append({
                            "message_id": msg_id,
                            "date": date_,
                            "from": from_,
                            "company": co,
                            "subject": subject,
                            "cls": cls,
                            "snippet": subject
                        })

        mail.logout()

        os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            for t in threads:
                f.write(json.dumps(t) + "\n")

        print(f"Synced {len(threads)} relevant recruitment threads to {OUT_FILE}")
        return threads

    except Exception as e:
        print(f"Gmail sync failed: {e}", file=sys.stderr)
        return []

if __name__ == "__main__":
    sync_gmail()
