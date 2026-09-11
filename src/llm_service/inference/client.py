from typing import Any

import httpx


class VLLMClient:
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: float = 120.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except httpx.HTTPError:
            return False

    async def models(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/v1/models")
            response.raise_for_status()
            return response.json()

    async def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 256,
    ) -> dict[str, Any]:

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
            )

            response.raise_for_status()
            return response.json()