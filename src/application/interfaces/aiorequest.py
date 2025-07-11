from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from src.application.dtos.response import Response


class AioRequest(ABC):
    @abstractmethod
    async def get(
        self,
        url: str,
        headers: Dict[str, str],
        data: Optional[Dict[str, Any]] = None
    ) -> Response[Any]:
        ...

    @abstractmethod
    async def post(
        self,
        url: str,
        headers: Dict[str, str],
        data: Optional[Dict[str, Any]] = None
    ) -> Response[Any]:
        ...

    @abstractmethod
    async def delele(
        self,
        url: str,
        headers: Dict[str, str],
        data: Dict[str, Any]
    ) -> Response[Any]:
        ...

    @abstractmethod
    async def patch(
        self,
        url: str,
        headers: Dict[str, str],
        data: Dict[str, Any]
    ) -> Response[Any]:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...
