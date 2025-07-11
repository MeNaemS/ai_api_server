from dishka import Provider, provide, Scope
from src.infrastructure.mappers.token import TokenMapper
from src.infrastructure.mappers.response_mapper import ResponseMapper


class MapperContainer(Provider):
    @provide(scope=Scope.APP)
    async def mapper_token(self) -> TokenMapper:
        return TokenMapper()

    @provide(scope=Scope.APP)
    async def mapper_response(self) -> ResponseMapper:
        return ResponseMapper()
