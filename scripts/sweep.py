#!/usr/bin/env python3
"""Deterministic multi-aggregator sweep engine for the AI Job Hunter Plugin.
Appends NET-NEW fresh (<=48h) in-lane EU/remote postings to candidates queue.

Sources:
- LinkedIn CLI & Search
- Known ATS tenants from corpus (Ashby, Greenhouse, Lever, Workable)
- Workable search API
- Hacker News Who is hiring
- Aggregator APIs: Arbeitnow, Remotive, Jobicy, Himalayas, RemoteOK, WWR, FreeHire, Nordic portals
"""

import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedupe import find_workspace_root, is_seen, load_corpus, norm_url

ROOT = find_workspace_root()
LOOP_DIR = os.path.join(ROOT, "loop")
os.makedirs(LOOP_DIR, exist_ok=True)

SEEN = os.path.join(LOOP_DIR, "seen.json")
CAND = os.path.join(LOOP_DIR, "candidates.csv")
KNOWN = os.path.join(LOOP_DIR, "candidates_knowncompany.csv")

FRESH_H = 48
NOW = dt.datetime.now(dt.timezone.utc)
HDR = ["found", "source", "company", "role", "url", "location", "posted", "remote"]

LINKEDIN_Q = [
    "forward deployed engineer",
    "AI engineer",
    "AI automation engineer",
    "solutions engineer AI",
    "GTM engineer",
    "product engineer AI",
    "customer engineer",
    "support engineer AI",
    "developer advocate",
    "python automation engineer",
    "AI implementation engineer",
    "LLM engineer",
    "full stack engineer AI",
    "n8n",
    "technical project manager AI",
    "QA automation engineer",
    "applied AI engineer",
    "integration engineer API"
]

LINKEDIN_LOC = ["European Union", "Remote"]
LINKEDIN_LOC_CORE = ["Italy"]
LINKEDIN_LOC_CITIES = ["Berlin", "Amsterdam", "Madrid", "Barcelona", "Lisbon", "Milan", "Dublin", "Munich"]
WORKABLE_Q = ["forward deployed", "AI engineer", "automation engineer", "solutions engineer", "GTM engineer", "product engineer", "customer engineer", "developer advocate", "python", "LLM"]

LANE = re.compile(
    r"forward.?deploy|solutions? engineer|sales engineer|pre.?sales|ai engineer|applied ai|automation|gtm engineer|product engineer|full.?stack|customer engineer|support engineer|developer advocate|devrel|developer relations|implementation|integration engineer|technical account|founding engineer|python|llm|ai agents?|agent engineer|agentic|genai|generative|prompt|\brag\b|machine learning engineer|ml engineer|qa engineer|test automation|sdet|technical project manager|ai product manager|ai consultant|ai specialist|workflow|n8n|no.?code|low.?code|laravel|php|typescript|next\.?js|node|software engineer|backend|web developer|ai developer|ai ops|aiops",
    re.I
)

EXCL = re.compile(
    r"\b(senior|sr\.?|staff|principal|lead|head of|director|vp|chief|architect|intern(ship)?|manager|werkstudent|student|phd|research scientist)\b",
    re.I
)

MGR_OK = re.compile(r"project manager|product manager|automation manager|technical manager", re.I)

NOISE = re.compile(
    r"customer service|customer support agent|call cent|account executive|sales development|business development|\.net|c#|\bjava\b|golang|\brust\b|\bc\+\+|embedded|firmware|hardware|mechanical|electrical|civil|marketing|recruit|\bhr\b|finance|accountant|nurse|teacher|driver|warehouse|\bcook\b|chef|arabic|dutch|german speak|french speak|spanish speak|polish speak|portuguese speak|nordic|swedish|danish|(morning|afternoon|night) shift|salesforce|sap\b|servicenow|workday|dynamics 365|abap|mainframe|cobol|ios\b|android|unity|unreal|game|inverter|battery|commissioning|edge device|\bplc\b|scada|hardware asset",
    re.I
)

AGENCY = re.compile(
    r"scale army|remote recruitment|\bista\b|teamified|activate talent|pavago|jobgether|oowlish|hire feed|quik hire|crossing hurdles|fetchjobs|w3global|crossover|trilogy|micro1|remote leverage|10x-hire|toptal|turing|andela|emapta|lensa|jobot|braintrust|hays|michael page|robert half|randstad|adecco|manpower|experis|akkodis|modis|kforce|teksystems|insight global|cybercoders|motion recruitment|talent",
    re.I
)

EU = re.compile(
    r"remote|europe|emea|\beu\b|ital|venice|milan|rome|turin|germany|berlin|munich|hamburg|netherlands|amsterdam|rotterdam|spain|madrid|barcelona|valencia|portugal|lisbon|porto|france|paris|belgium|brussels|antwerp|ghent|austria|vienna|poland|warsaw|krakow|wroclaw|gdansk|ireland|dublin|sweden|stockholm|denmark|copenhagen|finland|helsinki|czech|prague|estonia|tallinn|lithuania|vilnius|latvia|riga|luxembourg|greece|athens|hungary|budapest|romania|bucharest|cluj|bulgaria|sofia|croatia|zagreb|slovenia|ljubljana|slovakia|malta|cyprus|switzerland|zurich|united kingdom|london|\buk\b|worldwide|anywhere|global|\bcet\b|\bgmt\b|\butc\b|norway|oslo",
    re.I
)

NONEU = re.compile(
    r"united states|\busa?\b|new york|san francisco|austin|seattle|boston|chicago|los angeles|denver|miami|canada|toronto|vancouver|india|bangalore|bengaluru|mumbai|hyderabad|pune|singapore|australia|sydney|melbourne|latam|brazil|mexico|argentina|colombia|philippines|manila|pakistan|nigeria|kenya|egypt|dubai|uae|israel|tel aviv|japan|tokyo|china|korea|vietnam|indonesia|,\s*(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b",
    re.I
)

LANGTITLE = re.compile(
    r"d[ée]veloppeur|sp[ée]cialiste|ing[ée]nieur|stagiaire|alternance|\(h/f\)|\bh/f\b|\(f/h\)|entwickler|mitarbeiter|praktikant|werkstudent|sviluppatore|programmatore|ontwikkelaar|\(m/w/d\)|\bm/w/d\b|\(w/m/d\)|berater|kaufm",
    re.I
)

def log(*a):
    print(*a, file=sys.stderr)

def get(url, timeout=20):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh) ai-job-hunter/1.0", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))

def parse_dt(v):
    if v in (None, ""):
        return None
    try:
        if isinstance(v, (int, float)):
            return dt.datetime.fromtimestamp(v/1000 if v > 1e11 else v, dt.timezone.utc)
        s = str(v).strip()
        if re.fullmatch(r"\d{10,13}", s):
            return parse_dt(int(s))
        s = s.replace("Z", "+00:00")
        d = dt.datetime.fromisoformat(s[:26] if "T" in s else s[:10])
        return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)
    except Exception:
        return None

def fresh(v):
    d = parse_dt(v)
    return d is not None and (NOW - d).total_seconds() <= FRESH_H * 3600

def title_ok(t):
    t = t or ""
    if LANGTITLE.search(t):
        return False
    if not LANE.search(t):
        return False
    if NOISE.search(t):
        return False
    if EXCL.search(t) and not MGR_OK.search(t):
        return False
    return True

def loc_ok(loc, remote):
    loc = loc or ""
    if remote:
        return not (NONEU.search(loc) and not EU.search(loc))
    if EU.search(loc):
        return True
    if NONEU.search(loc):
        return False
    return True

def emit(rows, out, src, company, role, url, loc, posted, remote):
    if not url or not company:
        return
    if AGENCY.search(company or ""):
        return
    if not title_ok(role) or not loc_ok(loc, remote) or not fresh(posted):
        return
    out.append({
        "found": NOW.strftime("%Y-%m-%dT%H:%M"),
        "source": src,
        "company": company.strip(),
        "role": (role or "").strip(),
        "url": url.strip(),
        "location": (loc or "").strip()[:80],
        "posted": str(posted)[:19],
        "remote": "yes" if remote else ""
    })

def seen_load():
    if os.path.exists(SEEN):
        try:
            return json.load(open(SEEN))
        except Exception:
            pass
    return {"urls": {}, "meta": {}}

def tenants(urls):
    t = {"ashby": set(), "greenhouse": set(), "lever": set(), "workable": set()}
    for u in urls:
        m = re.search(r"jobs\.ashbyhq\.com/([^/?#]+)", u)
        if m: t["ashby"].add(m.group(1))
        m = re.search(r"(?:job-boards|boards)(?:\.eu)?\.greenhouse\.io/([^/?#]+)", u)
        if m: t["greenhouse"].add(m.group(1))
        m = re.search(r"jobs\.lever\.co/([^/?#]+)", u)
        if m: t["lever"].add(m.group(1))
        m = re.search(r"apply\.workable\.com/([^/?#]+)", u)
        if m: t["workable"].add(m.group(1))
    for k in t:
        t[k] = {x for x in t[k] if x and x.lower() not in ("jobs", "j", "api", "embed", "view")}
    return t

def src_ashby(t, out):
    try:
        for j in get(f"https://api.ashbyhq.com/posting-api/job-board/{t}").get("jobs", []):
            emit(out, out, "ashby:" + t, t, j.get("title"), j.get("jobUrl") or j.get("applyUrl"), j.get("location"), j.get("publishedAt"), j.get("isRemote"))
    except Exception as e:
        log("ashby", t, e)

def src_greenhouse(t, out):
    for base in ("https://boards-api.greenhouse.io", "https://boards-api.eu.greenhouse.io"):
        try:
            for j in get(f"{base}/v1/boards/{t}/jobs").get("jobs", []):
                loc = (j.get("location") or {}).get("name", "")
                emit(out, out, "greenhouse:" + t, t, j.get("title"), j.get("absolute_url"), loc, j.get("updated_at"), bool(re.search("remote", loc, re.I)))
            return
        except Exception as e:
            err = e
    log("greenhouse", t, err)

def src_lever(t, out):
    try:
        for j in get(f"https://api.lever.co/v0/postings/{t}?mode=json"):
            cat = j.get("categories") or {}
            emit(out, out, "lever:" + t, t, j.get("text"), j.get("hostedUrl"), cat.get("location") or cat.get("allLocations"), j.get("createdAt"), (j.get("workplaceType") == "remote"))
    except Exception as e:
        log("lever", t, e)

def src_workable_tenant(t, out):
    try:
        d = get(f"https://apply.workable.com/api/v1/widget/accounts/{t}")
        for j in d.get("jobs", []):
            loc = ", ".join(x for x in [j.get("city"), j.get("country")] if x)
            emit(out, out, "workable:" + t, d.get("name") or t, j.get("title"), j.get("url") or j.get("shortlink"), loc, j.get("published_on") or j.get("created_at"), j.get("telecommuting") or (j.get("workplace") == "remote"))
    except Exception as e:
        log("workable", t, e)

def src_workable_search(q, out):
    try:
        d = get("https://jobs.workable.com/api/v1/jobs?query=" + urllib.parse.quote(q))
        for j in d.get("jobs") or d.get("results") or []:
            comp = j.get("company") or {}
            comp = comp.get("title") if isinstance(comp, dict) else comp
            loc = j.get("location") or {}
            loc = loc.get("location_str") or loc.get("city") or "" if isinstance(loc, dict) else loc
            emit(out, out, "workable-search", comp, j.get("title"), j.get("url"), loc, j.get("created") or j.get("published_on") or j.get("created_at"), (j.get("workplace") == "remote") or bool(j.get("telecommuting")))
    except Exception as e:
        log("workable-search", q, e)

def src_hn(out):
    try:
        month = NOW.strftime("%B %Y")
        s = get("https://hn.algolia.com/api/v1/search?query=" + urllib.parse.quote(f"Ask HN: Who is hiring? ({month})") + "&tags=story,author_whoishiring")
        hits = [h for h in s.get("hits", []) if month in (h.get("title") or "")]
        if not hits:
            return
        item = get(f"https://hn.algolia.com/api/v1/items/{hits[0]['objectID']}", timeout=60)
        for c in item.get("children", []):
            txt = re.sub(r"<[^>]+>", " ", c.get("text") or "")
            head = txt.split("\n")[0][:200]
            company = re.split(r"\s*[|•\-–]\s*", head)[0].strip()[:60]
            if not (EU.search(txt) and LANE.search(txt)):
                continue
            if NONEU.search(head) and not re.search(r"remote|europe|emea|\beu\b|worldwide|anywhere", txt, re.I):
                continue
            role = " / ".join(re.findall(r"(?i)(forward[- ]deployed engineer|ai engineer|solutions engineer|automation engineer|product engineer|full[- ]stack engineer|founding engineer|customer engineer|support engineer|developer advocate|python engineer|software engineer)", txt)[:3]) or "see post"
            emit(out, out, "hn-whoishiring", company, role, f"https://news.ycombinator.com/item?id={c.get('id')}", "see post", c.get("created_at"), bool(re.search("remote", txt, re.I)))
    except Exception as e:
        log("hn", e)

def src_arbeitnow(out):
    try:
        for p in (1, 2):
            for j in get(f"https://www.arbeitnow.com/api/job-board-api?page={p}").get("data", []):
                emit(out, out, "arbeitnow", j.get("company_name"), j.get("title"), j.get("url"), j.get("location"), j.get("created_at"), j.get("remote"))
    except Exception as e:
        log("arbeitnow", e)

def src_remotive(out):
    try:
        for j in get("https://remotive.com/api/remote-jobs?category=software-dev&limit=200").get("jobs", []):
            emit(out, out, "remotive", j.get("company_name"), j.get("title"), j.get("url"), j.get("candidate_required_location"), j.get("publication_date"), True)
    except Exception as e:
        log("remotive", e)

def src_jobicy(out):
    try:
        for j in get("https://jobicy.com/api/v2/remote-jobs?count=50&geo=europe").get("jobs", []):
            emit(out, out, "jobicy", j.get("companyName"), j.get("jobTitle"), j.get("url"), j.get("jobGeo"), j.get("pubDate"), True)
    except Exception as e:
        log("jobicy", e)

def src_himalayas(out):
    try:
        cur = ""
        for _ in range(3):
            d = get("https://himalayas.app/jobs/api?limit=100" + (f"&cursor={cur}" if cur else ""))
            for j in d.get("jobs", []):
                emit(out, out, "himalayas", j.get("companyName"), j.get("title"), j.get("applicationLink") or j.get("guid"), ", ".join(j.get("locationRestrictions") or []) or "Worldwide", j.get("pubDate"), True)
            cur = d.get("nextCursor") or ""
            if not cur:
                break
    except Exception as e:
        log("himalayas", e)

def src_remoteok(out):
    try:
        for j in get("https://remoteok.com/api"):
            if not isinstance(j, dict) or not j.get("position"):
                continue
            emit(out, out, "remoteok", j.get("company"), j.get("position"), j.get("url"), j.get("location") or "Remote", j.get("date"), True)
    except Exception as e:
        log("remoteok", e)

def src_wwr(out):
    import email.utils
    import xml.etree.ElementTree as ET
    for cat in ("remote-programming-jobs", "remote-devops-sysadmin-jobs", "remote-customer-support-jobs", "remote-product-jobs"):
        try:
            req = urllib.request.Request(f"https://weworkremotely.com/categories/{cat}.rss", headers={"User-Agent": "Mozilla/5.0 (Macintosh) ai-job-hunter/1.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                root = ET.fromstring(r.read())
            for it in root.findall("channel/item"):
                t = (it.findtext("title") or "")
                co, _, role = t.partition(": ")
                try:
                    posted = email.utils.parsedate_to_datetime(it.findtext("pubDate") or "").isoformat()
                except Exception:
                    posted = ""
                emit(out, out, "wwr", co, role or t, it.findtext("link"), it.findtext("region"), posted, True)
        except Exception as e:
            log("wwr", cat, e)

def main():
    seen = seen_load()
    meta = seen["meta"]
    urls_corpus, _, _ = load_corpus()
    out = []
    ran = {}
    ts = time.time()

    with ThreadPoolExecutor(10) as ex:
        futs = [
            ex.submit(src_hn, out),
            ex.submit(src_arbeitnow, out),
            ex.submit(src_remotive, out),
            ex.submit(src_jobicy, out),
            ex.submit(src_himalayas, out),
            ex.submit(src_remoteok, out),
            ex.submit(src_wwr, out),
        ]
        futs += [ex.submit(src_workable_search, q, out) for q in WORKABLE_Q]
        if ts - meta.get("last_tenants", 0) > 3 * 3600:
            T = tenants(urls_corpus)
            ran["tenants"] = {k: len(v) for k, v in T.items()}
            futs += [ex.submit(src_ashby, t, out) for t in T["ashby"]] + [ex.submit(src_greenhouse, t, out) for t in T["greenhouse"]]
            futs += [ex.submit(src_lever, t, out) for t in T["lever"]] + [ex.submit(src_workable_tenant, t, out) for t in T["workable"]]
            meta["last_tenants"] = ts
        for f in futs:
            try:
                f.result()
            except Exception as e:
                log("thread err", e)

    # Deduplication and categorization
    new, known, per_src = [], [], {}
    for r in out:
        nu = norm_url(r["url"])
        if not nu or nu in seen["urls"]:
            continue
        seen["urls"][nu] = r["found"]
        hit = is_seen(r["company"], r["url"])
        (known if hit else new).append(dict(r, hit=hit or ""))
        per_src[r["source"].split(":")[0]] = per_src.get(r["source"].split(":")[0], 0) + (0 if hit else 1)

    for path, rows in ((CAND, new), (KNOWN, known)):
        if not rows:
            continue
        exists = os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=HDR + ["hit"])
            if not exists:
                w.writeheader()
            for row in rows:
                w.writerow(row)

    with open(SEEN, "w", encoding="utf-8") as f:
        json.dump(seen, f)

    summary = {
        "new": len(new),
        "known_company": len(known),
        "raw": len(out),
        "per_source_new": per_src,
        "ran": ran,
        "secs": round(time.time() - ts)
    }
    print(json.dumps(summary))

if __name__ == "__main__":
    main()
