from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from app.core.config import DatabaseConfig
from app.core.environment import Environment
from app.api.v1 import auth_router
from app.api.v1 import health_check
from fastapi.logger import logger
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache

db_instance = DatabaseConfig()


@lru_cache
def get_env():
    return Environment()


# Life cycle events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("1 Creating database and tables...")
    try:
        if get_env().OVERWRITE_DB:
            db_instance.drop_db()
        print("Creating database and tables...")
        db_instance.create_db_and_tables()
    except Exception as e:
        logger.error(f"Error during startup: {e}")
    yield
    # Shutdown


app = FastAPI(
    title="Task app",
    description="A simple task management API",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Routes
@app.get("/env", tags=["root"])
def get_env_path():
    return {"ENV": get_env().model_dump()}


app.include_router(health_check.router, prefix="/api/v1", tags=["health_check"])
app.include_router(auth_router.router, prefix="/api/v1", tags=["auth"])
