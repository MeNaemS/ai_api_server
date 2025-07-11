from dishka import Provider, Scope, provide
from src.config_schema import Config
from src.infrastructure.request.httpx_request import HttpxRequest
from src.infrastructure.mappers.response_mapper import ResponseMapper
from src.application.interfaces.aiorequest import AioRequest


class AIIntegrationContainer(Provider):
    @provide(scope=Scope.APP)
    async def https_request(self, config: Config, response_mapper: ResponseMapper) -> AioRequest:
        return HttpxRequest(config, response_mapper)
