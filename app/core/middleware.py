from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

def setup_cors(app: FastAPI):
    """
    Set up CORS middleware.
    """
    logger.info("Configuring CORS middleware...")
    app.add_middleware(
        CORSMiddleware,
        allow_origins="http://localhost:3000" or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS configured with origins: {settings.ALLOWED_ORIGINS or ['*']}")

def setup_middleware(app: FastAPI):
    """
    Set up middleware for the FastAPI app.
    """
    logger.info("Setting up middleware...")
    setup_cors(app)
    logger.info("Middleware setup complete.")
