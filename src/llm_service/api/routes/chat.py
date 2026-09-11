from fastapi import APIRouter, HTTPException

from llm_service.api.schemas.requests import ChatRequest
from llm_service.api.schemas.responses import ChatResponse
from llm_service.inference.service import InferenceService


router = APIRouter(prefix="/api/v1", tags=["chat"])

inference_service = InferenceService()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:

    try:
        messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.messages
        ]

        result = await inference_service.generate(
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        choice = result["choices"][0]
        message = choice["message"]

        return ChatResponse(
            id=result["id"],
            model=result["model"],
            content=message["content"],
            usage=result.get("usage"),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Inference service error: {exc}",
        ) from exc