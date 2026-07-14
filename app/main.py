from fastapi import FastAPI

from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.get("/", tags=["Root"])
async def root() -> dict[str , str]:
    return {
        "message": f"Welcome to {settings.APP_NAME}",
    }


@app.get("/health", tags=["Health"])
async def health() -> dict[str , str]:
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/health/live", tags=["Health"])
async def liveness() -> dict[str , str]:
    return {
        "status": "alive",
    }


@app.get("/health/ready", tags=["Health"])
async def readiness() -> dict[str , str]:
    return {
        "status": "ready",
    }