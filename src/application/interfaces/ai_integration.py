from abc import ABC, abstractmethod
from typing import Any
from src.application.dtos.request import ModelInfo
from src.application.dtos.response import Response


class ManagerAIIntegration(ABC):
    @abstractmethod
    async def get_current_api_key(self):
        ...

    @abstractmethod
    async def get_api_keys(self):
        ...

    @abstractmethod
    async def create_api_key(self, name: str, limit: float):
        ...

    @abstractmethod
    async def get_api_key(self, hash: str):
        ...

    @abstractmethod
    async def delete_api_key(self, hash: str):
        ...

    @abstractmethod
    async def update_api_key(self, hash: str, name: str, disabled: bool, limit: float):
        ...


class AIIntegration(ABC):
    @abstractmethod
    async def chat(self, token: str, model_info: ModelInfo) -> Response[Any]:
        ...

    @abstractmethod
    async def get_credits(self, token: str) -> Response[Any]:
        ...

    @abstractmethod
    async def create_coinbase(
        self,
        token: str,
        amount: float,
        sender: str,
        chain_id: int
    ) -> Response[Any]:
        ...
