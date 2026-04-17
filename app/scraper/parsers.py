import requests
from bs4 import BeautifulSoup
from datetime import datetime

class BaseParser:
    def parse(self, url, company):
        raise NotImplementedError

class GreenhouseParser(BaseParser):
    def parse(self, url, company):
        # Greenhouse often has a JSON API: boards-api.greenhouse.io/v1/boards/{name}/jobs
        # But we'll try to scrape the HTML first as per the UI links
        norm = url.split("/")[-1]
        api_url = f"https://boards-api.greenhouse.io/v1/boards/{norm}/jobs"
        
        jobs = []
        try:
            r = requests.get(api_url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                for j in data.get("jobs", []):
                    jobs.append({
                        "title": j.get("title"),
                        "company": company,
                        "location": j.get("location", {}).get("name"),
                        "url": j.get("absolute_url"),
                        "description": None, # API requires another call for full content
                        "source": "greenhouse",
                        "posted_date": datetime.now() # API doesn't always provide posted date
                    })
        except Exception as e:
            print(f"Error parsing Greenhouse {company}: {e}")
            
        return jobs

class LeverParser(BaseParser):
    def parse(self, url, company):
        # Lever API: api.lever.co/v0/postings/{name}
        norm = url.split("/")[-1]
        api_url = f"https://api.lever.co/v0/postings/{norm}"
        
        jobs = []
        try:
            r = requests.get(api_url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                for j in data:
                    jobs.append({
                        "title": j.get("text"),
                        "company": company,
                        "location": j.get("categories", {}).get("location"),
                        "url": j.get("applyUrl"),
                        "description": j.get("descriptionPlain"),
                        "source": "lever",
                        "posted_date": datetime.fromtimestamp(j.get("createdAt") / 1000.0) if j.get("createdAt") else datetime.now()
                    })
        except Exception as e:
            print(f"Error parsing Lever {company}: {e}")
            
        return jobs

class ParserFactory:
    @staticmethod
    def get_parser(ats_type):
        if ats_type == "greenhouse":
            return GreenhouseParser()
        elif ats_type == "lever":
            return LeverParser()
        return None
