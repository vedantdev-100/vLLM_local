from fastapi import APIRouter

from llm_service.inference.service import InferenceService


router = APIRouter(tags=["health"])

inference_service = InferenceService()


@router.get("/health")
async def health():
    vllm_available = await inference_service.health()

    return {
        "status": "ok" if vllm_available else "degraded",
        "vllm": "up" if vllm_available else "down",
    }