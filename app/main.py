from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.db import Base, engine
from app.routes.jobs import router as jobs_router

app = FastAPI(title="Internship Search Backend")

# Create tables
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth_router)

app.include_router(jobs_router)

@app.get("/")
def root():
    return {"status": "backend running"}
