import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
# We'll use a popular embedding model like sentence-transformers
MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{MODEL_ID}"

class HFClient:
    def __init__(self, token=HF_TOKEN):
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def get_embeddings(self, text):
        """
        Fetches embeddings for the given text using Hugging Face Inference API.
        """
        if not self.token:
            # Fallback or error if token is missing
            print("Warning: HF_TOKEN missing. Embedding will fail.")
            return None
            
        try:
            response = requests.post(API_URL, headers=self.headers, json={"inputs": text})
            if response.status_code == 200:
                return response.json()
            else:
                print(f"HF API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error calling HF API: {e}")
            return None
