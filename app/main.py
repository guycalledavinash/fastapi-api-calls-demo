"""FastAPI application factory and route registration."""

from fastapi import FastAPI

from app.routes import external_api, users
from app.schemas import HealthCheck

app = FastAPI(
    title="FastAPI API Calls Demo",
    summary="A small demo that wraps GitHub and JSONPlaceholder APIs.",
    version="1.0.0",
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(external_api.router, prefix="/external", tags=["External APIs"])


@app.get("/", response_model=HealthCheck)
def root() -> HealthCheck:
    """Basic health check for load balancers and humans."""
    return HealthCheck(message="FastAPI API call demo is working!")
