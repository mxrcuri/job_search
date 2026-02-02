from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import get_db
from app.db_models import Job, JobSave, User
from app.db_schemas import JobOut
from app.routes.auth import get_current_user

router = APIRouter(prefix="/jobs", tags=["jobs"])

# --------------------------------------------------
# 1️⃣ GET /jobs → list all jobs (PUBLIC)
# --------------------------------------------------
@router.get("/", response_model=list[JobOut])
def list_jobs(
    db: Session = Depends(get_db),
):
    jobs = db.query(Job).order_by(Job.scraped_at.desc()).all()
    return jobs


# --------------------------------------------------
# 2️⃣ POST /jobs/{id}/save → save job (PROTECTED)
# --------------------------------------------------
@router.post("/{job_id}/save", status_code=status.HTTP_201_CREATED)
def save_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    existing = (
        db.query(JobSave)
        .filter(
            JobSave.user_id == current_user.id,
            JobSave.job_id == job_id
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Job already saved"
        )

    save = JobSave(user_id=current_user.id, job_id=job_id)
    db.add(save)
    db.commit()

    return {"message": "Job saved"}


# --------------------------------------------------
# 3️⃣ GET /jobs/saved → list saved jobs (PROTECTED)
# --------------------------------------------------
@router.get("/saved", response_model=list[JobOut])
def list_saved_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    jobs = (
        db.query(Job)
        .join(JobSave, Job.id == JobSave.job_id)
        .filter(JobSave.user_id == current_user.id)
        .order_by(JobSave.saved_at.desc())
        .all()
    )

    return jobs


# --------------------------------------------------
# 4️⃣ DELETE /jobs/{id}/unsave → unsave job (PROTECTED)
# --------------------------------------------------
@router.delete("/{job_id}/unsave", status_code=status.HTTP_204_NO_CONTENT)
def unsave_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    saved = (
        db.query(JobSave)
        .filter(
            JobSave.user_id == current_user.id,
            JobSave.job_id == job_id
        )
        .first()
    )

    if not saved:
        raise HTTPException(status_code=404, detail="Saved job not found")

    db.delete(saved)
    db.commit()

@router.post("/seed")
def seed_jobs(db: Session = Depends(get_db)):
    jobs = [
        Job(
            title="Software Intern",
            company="Google",
            location="Remote",
            description="Backend intern role",
            url="https://example.com/google-intern",
            source="manual"
        ),
        Job(
            title="ML Intern",
            company="Microsoft",
            location="India",
            description="ML internship",
            url="https://example.com/ms-intern",
            source="manual"
        )
    ]

    db.add_all(jobs)
    db.commit()

    return {"message": "Seeded jobs"}
