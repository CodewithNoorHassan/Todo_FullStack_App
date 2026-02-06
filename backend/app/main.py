import os
import sys
from dotenv import load_dotenv

# Load environment variables before importing settings
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Add the backend directory to the path to allow absolute imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.health import router as health_router
from app.middleware import add_error_handling_middleware

# Import routers using absolute imports
from routers.task import router as task_router
from routers.auth import router as auth_router
from routers.todo import router as todo_router
from routers.dashboard import router as dashboard_router
from security.middleware import add_security_middleware
from logging_config.config import setup_comprehensive_logging


def create_app() -> FastAPI:
    # Set up comprehensive logging
    setup_comprehensive_logging()

    app = FastAPI(
        title="TaskMaster API",
        description="Premium Todo Application Backend API",
        version="1.0.0",
        debug=(settings.APP_ENV == "development")
    )

    # Add security middleware first (highest priority)
    add_security_middleware(app)

    # Add error handling middleware
    add_error_handling_middleware(app)

    # Add CORS middleware for frontend integration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # expose_headers=["Access-Control-Allow-Origin"]
    )

    # Include health check router
    app.include_router(health_router)

    # Include task router
    app.include_router(task_router)

    # Include todo router
    app.include_router(todo_router)
    # Include dashboard router
    app.include_router(dashboard_router)

    # Include auth router
    app.include_router(auth_router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=(settings.APP_ENV == "development")
    )