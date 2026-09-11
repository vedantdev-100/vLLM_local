from fastapi import APIRouter

from llm_service.inference.service import InferenceService


router = APIRouter(tags=["models"])

inference_service = InferenceService()


@router.get("/models")
async def models():
    return await inference_service.models()