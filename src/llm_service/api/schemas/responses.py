from typing import Any

from pydantic import BaseModel


class ChatResponse(BaseModel):
    id: str
    model: str
    content: str
    usage: dict[str, Any] | None = None