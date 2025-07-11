from dataclasses import dataclass
from typing import List, Literal


@dataclass(slots=True)
class Message:
    role: Literal["user", "assistant", "system"]
    content: str


@dataclass(slots=True)
class ModelInfo:
    model: str
    messages: List[Message]
    stream: bool
    temperature: float
    top_p: float
