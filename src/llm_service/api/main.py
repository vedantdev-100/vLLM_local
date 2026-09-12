from contextlib import asynccontextmanager

from fastapi import FastAPI

from llm_service.api.middleware import RequestIDMiddleware
from llm_service.api.routes.chat import router as chat_router
from llm_service.api.routes.health import router as health_router
from llm_service.api.routes.models import router as models_router
from llm_service.core.config import settings
from llm_service.core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.log_level)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)

app.include_router(health_router)
app.include_router(models_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "status": "running",
    }