from fastapi import FastAPI

from llm_service.api.routes.chat import router as chat_router
from llm_service.api.routes.health import router as health_router
from llm_service.api.routes.models import router as models_router
from llm_service.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)


app.include_router(health_router)
app.include_router(models_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "service": settings.app_name,
        "status": "running",
    }