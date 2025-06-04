from dishka import Provider, provide, Scope
from src.infrastructure.mappers.token import TokenMapper


class MapperContainer(Provider):
    @provide(scope=Scope.APP)
    async def mapper_token(self) -> TokenMapper:
        return TokenMapper()
