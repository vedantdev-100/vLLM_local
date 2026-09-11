from typing import Any

from llm_service.core.config import settings
from llm_service.inference.client import VLLMClient


class InferenceService:
    def __init__(self):
        self.client = VLLMClient(
            base_url=settings.vllm_base_url,
            timeout=settings.request_timeout,
        )

    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> dict[str, Any]:

        return await self.client.chat_completion(
            model=settings.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def health(self) -> bool:
        return await self.client.health()

    async def models(self) -> dict[str, Any]:
        return await self.client.models()