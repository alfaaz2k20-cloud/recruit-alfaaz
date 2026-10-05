from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db

# Include the recruit router
from app.routers.recruit import router as recruit_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    init_db()
    yield
    # Runs on shutdown (nothing needed here yet)


app = FastAPI(
    title="Alfaaz Recruit API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recruit_router)


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"service": "Alfaaz Recruit", "status": "running"}
