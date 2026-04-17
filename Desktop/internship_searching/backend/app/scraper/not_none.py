import json

INPUT_FILE = "company_ats.json"
OUTPUT_FILE = "company_ats_filtered.json"

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

# Keep only entries where ats is not "none"
filtered = {
    company: info
    for company, info in data.items()
    if info.get("ats") != "none"
}

# Save filtered results
with open(OUTPUT_FILE, "w") as f:
    json.dump(filtered, f, indent=2)

print(f"Original count: {len(data)}")
print(f"Filtered count (non-none): {len(filtered)}")
print("Saved to company_ats_filtered.json")

