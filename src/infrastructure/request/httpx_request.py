from src.application.interfaces.aiorequest import AioRequest
from src.application.dtos.response import Response
from src.infrastructure.mappers.response_mapper import ResponseMapper
from src.config_schema import Config
from httpx import AsyncClient
from typing import Optional, Dict, Any


class HttpxRequest(AioRequest):
    def __init__(self, config: Config, response_mapper: ResponseMapper):
        self.config: Config = config
        self.client: AsyncClient = AsyncClient(
            headers={
                "Content-Type": "application/json",
            }
        )
        self.response_mapper: ResponseMapper = response_mapper

    async def get(
        self,
        url: str,
        headers: Dict[str, str],
        data: Optional[Dict[str, Any]] = None
    ) -> Response[Any]:
        return await self.response_mapper.to_response(
            await self.client.get(url, headers=headers, params=data)
        )

    async def post(
        self,
        url: str,
        headers: Dict[str, str],
        data: Dict[str, Any]
    ) -> Response[Any]:
        return await self.response_mapper.to_response(
            await self.client.post(url, json=data, headers=headers)
        )

    async def delele(
        self,
        url: str,
        headers: Dict[str, str],
        data: Dict[str, Any]
    ) -> Response[Any]:
        return await self.response_mapper.to_response(
            await self.client.delete(url, headers=headers, params=data)
        )

    async def patch(
        self,
        url: str,
        headers: Dict[str, str],
        data: Dict[str, Any]
    ) -> Response[Any]:
        return await self.response_mapper.to_response(
            await self.client.patch(url, headers=headers, json=data)
        )

    async def close(self) -> None:
        await self.client.aclose()
