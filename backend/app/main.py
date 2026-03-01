from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.assessments import router as assessments_router

app = FastAPI(
    title="SVAT API",
    description="Site Viability Assessment Tool — data-driven site assessment for green hydrogen projects. US only (MVP).",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assessments_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
