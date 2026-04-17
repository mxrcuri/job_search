from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db import get_db
from app.db_models import Job
from app.ml.resume_matcher import ResumeMatcher
from app.db_schemas import JobOut

router = APIRouter(prefix="/ml", tags=["ml"])
matcher = ResumeMatcher()

@router.post("/match", response_model=list[dict])
def match_resume(
    resume_text: str, # For simplicity, we'll take raw text. Could be file upload.
    db: Session = Depends(get_db)
):
    """
    Given a resume text, return the top matching jobs.
    """
    jobs = db.query(Job).all()
    if not jobs:
        return []
        
    results = matcher.match(resume_text, jobs)
    
    # Format response
    output = []
    for res in results[:10]: # Top 10
        job_data = JobOut.from_orm(res["job"])
        output.append({
            "score": round(res["score"], 4),
            "job": job_data
        })
        
    return output

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Endpoint to handle resume file upload and extract text.
    (Currently returns dummy text for demonstration)
    """
    content = await file.read()
    # In a real app, use a library like PyPDF2 or pdfminer to extract text
    return {"filename": file.filename, "extracted_text": "Sample resume text extracted from PDF."}
