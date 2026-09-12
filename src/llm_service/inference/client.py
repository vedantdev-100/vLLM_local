from typing import Any

import httpx

from llm_service.core.exceptions import (
    InferenceTimeoutError,
    InferenceUnavailableError,
)


class VLLMClient:

    def __init__(
        self,
        base_url: str,
        timeout: float = 120.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.base_url}/health"
                )

                return response.status_code == 200

        except httpx.HTTPError:
            return False

    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> dict[str, Any]:

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            async with httpx.AsyncClient(
                timeout=self.timeout
            ) as client:

                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload,
                )

                response.raise_for_status()

                return response.json()

        except httpx.TimeoutException as exc:
            raise InferenceTimeoutError(
                "vLLM request timed out"
            ) from exc

        except httpx.HTTPError as exc:
            raise InferenceUnavailableError(
                "vLLM is unavailable"
            ) from exc