import requests
import json
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

TIMEOUT = 2
MAX_THREADS = 50
WORKDAY_INSTANCES = [f"wd{i}" for i in range(1, 13)]


# ----------------------------
# Normalize names
# ----------------------------
def normalize(company):
    return re.sub(r"[^a-z0-9]", "", company.lower())


# ----------------------------
# Find Workday API endpoint
# ----------------------------
def find_workday_api(company_name):

    norm = normalize(company_name)
    pascal = company_name.title().replace(" ", "")
    upper = company_name.upper().replace(" ", "")

    site_guesses = [
        norm, pascal, upper,
        "external", "External",
        "jobs", "Jobs",
        "external_experienced",
        "ExternalCareerSite",
        "External_Career_Site",
        f"{pascal}External",
        f"{pascal}Jobs",
        f"{pascal}CareerSite",
        f"{pascal}ExternalCareerSite",
        f"{upper}ExternalCareerSite",
        f"{upper}Jobs",
    ]

    # 🔥 guess wd instance + site
    for wd in WORKDAY_INSTANCES:

        base = f"https://{norm}.{wd}.myworkdayjobs.com"

        for site in site_guesses:

            candidate = f"{base}/wday/cxs/{norm}/{site}/jobs"

            try:
                r = requests.post(candidate, json={"limit": 1}, headers=HEADERS, timeout=TIMEOUT)

                if r.status_code == 200:
                    print(f"✅ {company_name} → {candidate}")
                    return candidate

            except:
                pass

    print(f"❌ {company_name} → not Workday")
    return None


# ----------------------------
# Worker
# ----------------------------
def process(company):
    return company, find_workday_api(company)


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":

    df = pd.read_csv("unique_companies.csv")  # ONLY "Company Names"
    companies = df["Company Name"].dropna().unique()

    results = {}

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(process, c) for c in companies]

        for f in as_completed(futures):
            company, api = f.result()
            if api:
                results[company] = api

    with open("workday_api_urls.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Saved endpoints to workday_api_urls.json")

