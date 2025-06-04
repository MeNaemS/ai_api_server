from src.infrastructure.dtos.token import Token


class TokenMapper:
    @staticmethod
    async def to_token_model(access_token: str, token_type: str, expire: int) -> Token:
        return Token(
            access_token=access_token,
            token_type=token_type,
            expire=expire
        )
