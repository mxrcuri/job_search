from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.db import Base, engine
from app.routes.jobs import router as jobs_router
from app.routes.ml import router as ml_router
from app.scraper.runner import start_scheduler, shutdown_scheduler

app = FastAPI(title="Internship Search Backend")

# Create tables
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    start_scheduler()

@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()

# Routers
app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(ml_router)

@app.get("/")
def root():
    return {"status": "backend running"}
