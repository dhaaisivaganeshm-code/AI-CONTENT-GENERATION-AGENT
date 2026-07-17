import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import connect_db, close_db
from app.routers import auth, chat


logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """

    # Startup
    logger.info("Starting AI Content Assistant API...")

    await connect_db()

    yield

    # Shutdown
    logger.info("Shutting down API...")

    await close_db()



app = FastAPI(
    title="AI Content Assistant API",
    description="AI powered content generation backend",
    version="1.0.0",
    lifespan=lifespan,
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ==========================
# API Routes
# ==========================

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"],
)


app.include_router(
    chat.router,
    prefix="/api/chat",
    tags=["Chat"],
)



@app.get(
    "/api/health",
    tags=["Health"],
)
async def health_check():

    return {
        "status": "healthy",
        "service": "AI Content Assistant API",
    }