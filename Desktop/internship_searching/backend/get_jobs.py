import time
import pandas as pd
from jobspy import scrape_jobs

# 1. EXPANDED KEYWORD LIST (To reach 1000+)
# Mix of broad and niche terms based on your fields
search_terms = [
    # CS/IT
    "Software Intern", "Web Developer Intern", "Data Science Intern", 
    "AI Intern", "Machine Learning", "ReactJS", "NodeJS", "DevOps",
    # Electronics (ET/ECE)
    "Embedded Engineer", "VLSI", "IOT Intern", "Robotics",
    # Core/Other
    "Chemical Engineering Intern", "Biotech Intern", "Business Analyst",
    "Product Management", "HR Intern", "Content Writing", "Graphic Design"
]

# 2. CITY LIST
locations = ["Bangalore", "Mumbai", "Hyderabad", "Pune", "Gurgaon", "Noida", "Chennai"]

all_jobs = []

for location in locations:
    for term in search_terms:
        print(f"Scraping {term} in {location}...")
        
        try:
            jobs = scrape_jobs(
                site_name=["indeed", "glassdoor", "naukri"], # LinkedIn is strictest, use carefully
                search_term=term,
                location=location,
                results_wanted=15,  # Small number per query is safer!
                country_indeed='India',
                job_type="internship",
                hours_old=24 # Only new jobs from the last day
            )
            
            # Add to list if we found anything
            if not jobs.empty:
                all_jobs.append(jobs)
                
            print(f"Found {len(jobs)} jobs.")
            
        except Exception as e:
            print(f"Error scraping {term} in {location}: {e}")
            
        # CRITICAL: Sleep for 10-20 seconds between searches to look human
        time.sleep(15)

# Combine all batch results
if all_jobs:
    final_df = pd.concat(all_jobs, ignore_index=True)
    
    # Remove duplicates (Same job might be listed in 'Software' and 'Python')
    final_df = final_df.drop_duplicates(subset=['job_url'])
    
    print(f"Total Unique Jobs Fetched: {len(final_df)}")
    final_df.to_csv(f"daily_jobs_{pd.Timestamp.now().date()}.csv", index=False)
