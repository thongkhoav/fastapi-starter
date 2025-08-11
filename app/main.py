from fastapi import FastAPI, Query
from app.db import database, base
from app.api.v1 import auth_router
from app.api.v1 import health_check

# Create tables
base.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Task app")

# Routes
app.include_router(health_check.router, prefix="/api/v1", tags=["auth"])
app.include_router(auth_router.router, prefix="/api/v1", tags=["auth"])
