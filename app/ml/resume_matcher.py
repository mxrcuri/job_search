import math
from app.ml.hf_client import HFClient

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def magnitude(v):
    return math.sqrt(sum(x * x for x in v))

def cosine_similarity(v1, v2):
    m1 = magnitude(v1)
    m2 = magnitude(v2)
    if m1 == 0 or m2 == 0:
        return 0
    return dot_product(v1, v2) / (m1 * m2)

class ResumeMatcher:
    def __init__(self):
        self.hf_client = HFClient()

    def match(self, resume_text, jobs):
        """
        Rank jobs based on their similarity to the resume text.
        """
        resume_embedding = self.hf_client.get_embeddings(resume_text)
        if not resume_embedding:
            return []
            
        ranked_jobs = []
        for job in jobs:
            # Combine title and description for embedding
            job_text = f"{job.title} {job.description or ''}"
            job_embedding = self.hf_client.get_embeddings(job_text)
            
            if job_embedding:
                score = cosine_similarity(resume_embedding, job_embedding)
                ranked_jobs.append({
                    "job": job,
                    "score": score
                })
        
        # Sort by score descending
        ranked_jobs.sort(key=lambda x: x["score"], reverse=True)
        return ranked_jobs
