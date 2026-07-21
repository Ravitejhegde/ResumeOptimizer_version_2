from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.routes.resume import router as resume_router
from app.api.routes.job_description import router as job_router
from app.api.routes.analysis import router as analysis_router
from app.api.routes.optimization import router as optimization_router
from app.api.routes.download import (
    router as download_router,
)
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(job_router)
app.include_router(analysis_router)
app.include_router(optimization_router)
app.include_router(
    download_router
)

@app.on_event("startup")
async def startup():
    settings.TEMP_DIR.mkdir(parents=True, exist_ok=True)
    settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    settings.EXPORT_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }