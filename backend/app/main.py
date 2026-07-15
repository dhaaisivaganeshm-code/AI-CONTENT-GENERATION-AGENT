from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import connect_db, close_db
from app.routers import auth, chat


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    await connect_db()

    yield

    # Shutdown
    await close_db()


app = FastAPI(
    title="AI Content Assistant API",
    version="1.0.0",
    lifespan=lifespan
)


origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes

app.include_router(
    auth.router,
    prefix="/api"
)

app.include_router(
    chat.router,
    prefix="/api"
)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "message": "AI Content Assistant API running"
    }