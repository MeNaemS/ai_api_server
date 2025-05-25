"""Main FastAPI application entry point."""
# ----- Imports -----
# FastAPI framework
from fastapi import FastAPI

# Dependency injection
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from dishka import make_async_container, AsyncContainer
from src.adapters.api.di.container import Container

# Application components
from src.infrastructure.logging.logger_setup import setup_logger
from src.adapters.api.routers.auth import router as auth_router
import logging


# ----- Logging Setup -----
setup_logger()
logger = logging.getLogger(__name__)

# ----- FastAPI Application Setup -----
logger.info("Initializing FastAPI application")
app: FastAPI = FastAPI(
    title="AI Bot API",
    description="API for AI Bot services",
    version="0.1.0",
)
logger.info("FastAPI application initialized")

# ----- Register Routers -----
app.include_router(auth_router)

# ----- Dependency Injection Setup -----
# Create async container with our DI container and FastAPI provider
container: AsyncContainer = make_async_container(Container(), FastapiProvider())

# Configure FastAPI to use our DI container
setup_dishka(app=app, container=container)
