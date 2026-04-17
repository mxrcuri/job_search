import requests
import pandas as pd
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

TIMEOUT = 5
WORKDAY_INSTANCES = ["wd1", "wd2", "wd3", "wd4", "wd5"]
MAX_THREADS = 25


# -------------------------
# Normalization (VERY IMPORTANT)
# -------------------------
def normalize(company):
    company = company.lower()
    company = re.sub(r"[&',\.]", "", company)
    company = re.sub(r"\s+", "-", company.strip())
    return company


# -------------------------
# ATS Detection
# -------------------------
def detect_ats(company):
    norm = normalize(company)

    # ---------- Greenhouse ----------
    gh_base = f"https://boards.greenhouse.io/{norm}"
    try:
        r = requests.get(gh_base, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code == 200:
            return {"ats": "greenhouse", "url": gh_base}
    except:
        pass

    # ---------- Workday (BASE DOMAIN ONLY) ----------
    for wd in WORKDAY_INSTANCES:
        wd_base = f"https://{norm}.{wd}.myworkdayjobs.com"
        try:
            r = requests.get(wd_base, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                return {"ats": "workday", "url": wd_base}
        except:
            continue

    # ---------- Lever ----------
    lever_base = f"https://jobs.lever.co/{norm}"
    try:
        r = requests.get(lever_base, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code == 200:
            return {"ats": "lever", "url": lever_base}
    except:
        pass

    # ---------- Default ----------
    return {"ats": "none", "url": None}


# -------------------------
# Worker
# -------------------------
def process(company):
    result = detect_ats(company)
    print(f"[{company}] → {result['ats']}")
    return company, result


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":

    df = pd.read_csv("unique_companies.csv")  # column: Company names
    companies = df["Company Name"].dropna().unique()

    results = {}

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(process, c) for c in companies]

        for f in as_completed(futures):
            company, res = f.result()
            results[company] = res

    with open("company_ats.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Done. Saved to company_ats.json")

