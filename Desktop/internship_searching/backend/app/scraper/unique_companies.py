import pandas as pd

# Read CSV
df = pd.read_csv('merged_companies.csv')

# Clean and deduplicate
df['Company Name'] = df['Company Name'].str.strip().str.lower()
df = df[df['Company Name'].notna() & (df['Company Name'] != '')]
unique_companies = df['Company Name'].drop_duplicates()

# Save or print
print("Total unique entries:", len(unique_companies))
unique_companies.to_csv('unique_companies.csv', index=False)

