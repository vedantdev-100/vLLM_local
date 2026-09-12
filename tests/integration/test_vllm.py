import pytest

from llm_service.inference.client import VLLMClient


@pytest.mark.asyncio
async def test_vllm_models():

    client = VLLMClient(
        base_url="http://localhost:8000"
    )

    models = await client.models()

    assert "data" in models
    assert len(models["data"]) > 0