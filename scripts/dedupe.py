#!/usr/bin/env python3
"""Multi-Tier Deduplication Engine for the AI Job Hunter Plugin.
Scans URLs, numeric job IDs, normalized company names, and brand aliases.

Usage:
  python3 dedupe.py --check "<Company>" ["<url>"]
  python3 dedupe.py --rebuild
"""

import csv
import glob
import json
import os
import re
import sys
from urllib.parse import parse_qsl

def find_workspace_root():
    cur = os.path.abspath(os.getcwd())
    while cur != os.path.dirname(cur):
        if os.path.exists(os.path.join(cur, "applications.csv")) or os.path.exists(os.path.join(cur, "loop")):
            return cur
        cur = os.path.dirname(cur)
    return os.path.abspath(os.getcwd())

ROOT = find_workspace_root()
CACHE = os.path.join(ROOT, "loop", "corpus.json")

SUFFIX = re.compile(
    r"\b(inc|ltd|limited|llc|gmbh|srl|s\.?p\.?a|s\.?r\.?l|sa|ag|bv|b\.v|plc|co|corp|group|technologies|technology|tech|labs|software|solutions|the)\b\.?",
    re.I
)

ALIASES = {
    "mau": "leadtech",
    "ai-lab": "leadtech",
    "mau / ai-lab": "leadtech",
    "mau ai-lab": "leadtech",
    "transcendent group": "advisense"
}

IDNUM = re.compile(r"(?<!\d)\d{7,}(?!\d)")

def norm_url(u):
    u = (u or "").strip().lower()
    if not u.startswith("http"):
        return ""
    u = re.sub(r"^https?://(www\.)?", "", u)
    path, _, qs = u.partition("?")
    path = path.split("#")[0].rstrip("/")
    job_params = {"jobid", "gh_jid", "job_id", "id", "req", "requisitionid", "jid", "posting"}
    return next((f"{path}?{k}={v}" for k, v in parse_qsl(qs) if k.lower() in job_params), path)

def norm_co(c):
    c = (c or "").strip().lower()
    c = re.sub(r"[.,()\[\]\"'’‘*]", " ", c)
    c = SUFFIX.sub(" ", c)
    c = re.sub(r"\s+", " ", c).strip()
    return ALIASES.get(c, c)

def _sources():
    files = [os.path.join(ROOT, "applications.csv")] + glob.glob(os.path.join(ROOT, "role-sweep-*.csv"))
    files += [
        os.path.join(ROOT, "MASTER - every application - 13 Aug 2026.xlsx"),
        os.path.join(ROOT, "Role shortlist - 8 Aug 2026.xlsx")
    ]
    return [f for f in files if os.path.exists(f)]

def build():
    urls, comps, ids = set(), set(), set()
    for f in _sources():
        if f.endswith(".csv"):
            with open(f, newline="", encoding="utf-8", errors="replace") as fh:
                for i, row in enumerate(csv.reader(fh)):
                    if i == 0:
                        continue
                    for cell in row:
                        nu = norm_url(cell)
                        if nu:
                            urls.add(nu)
                            ids.update(IDNUM.findall(nu))
                    if not row:
                        continue
                    key = row[1] if len(row) > 1 and "applications.csv" in f else row[0]
                    if len(row) > 1 and key and not key.startswith("http"):
                        nc = norm_co(key)
                        if nc:
                            comps.add(nc)
        else:
            try:
                import openpyxl
                wb = openpyxl.load_workbook(f, read_only=True)
                for ws in wb.worksheets:
                    for row in ws.iter_rows(values_only=True):
                        for cell in row:
                            if isinstance(cell, str):
                                nu = norm_url(cell)
                                if nu:
                                    urls.add(nu)
                                    ids.update(IDNUM.findall(nu))
                        idx = 1 if "MASTER" in f else 0
                        if len(row) > idx and isinstance(row[idx], str) and not row[idx].startswith("http") and len(row[idx]) < 80:
                            nc = norm_co(row[idx])
                            if nc and len(nc) > 1:
                                comps.add(nc)
            except Exception as e:
                pass
    junk = {"company", "date", "status", "role", "url", "ats", "notes", "prio", "link", "none", ""}
    comps = {c for c in comps if c not in junk}
    data = {
        "urls": sorted(urls),
        "ids": sorted(ids),
        "companies": sorted(comps),
        "mtimes": {f: os.path.getmtime(f) for f in _sources()}
    }
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return data

def load_corpus():
    if os.path.exists(CACHE):
        try:
            with open(CACHE, "r", encoding="utf-8") as f:
                d = json.load(f)
            if "ids" in d and all(os.path.getmtime(f) <= d.get("mtimes", {}).get(f, -1) for f in _sources()):
                return set(d["urls"]), set(d["companies"]), set(d["ids"])
        except Exception:
            pass
    d = build()
    return set(d["urls"]), set(d["companies"]), set(d["ids"])

_C = None
def is_seen(company, url=""):
    """Returns 'URL' | 'COMPANY' | 'COMPANY~' | None"""
    global _C
    if _C is None:
        _C = load_corpus()
    urls, comps, ids = _C
    nu = norm_url(url)
    if nu and nu in urls:
        return "URL"
    if nu and any(i in ids for i in IDNUM.findall(nu)):
        return "URL"
    nc = norm_co(company)
    if not nc:
        return None
    if nc in comps:
        return "COMPANY"
    if len(nc) >= 5:
        for k in comps:
            if len(k) >= 5 and (nc in k or k in nc):
                return "COMPANY~"
    return None

if __name__ == "__main__":
    if "--rebuild" in sys.argv:
        d = build()
        print("Rebuilt corpus:", len(d["urls"]), "URLs,", len(d["companies"]), "companies")
        sys.exit(0)
    if "--check" in sys.argv:
        i = sys.argv.index("--check")
        co = sys.argv[i+1] if len(sys.argv) > i+1 else ""
        url = sys.argv[i+2] if len(sys.argv) > i+2 else ""
        r = is_seen(co, url)
        print(("HIT " + r) if r else "NEW")
        sys.exit(0)
    u, c, i = load_corpus()
    print("Corpus status:", len(u), "URLs,", len(c), "companies,", len(i), "numeric IDs")
