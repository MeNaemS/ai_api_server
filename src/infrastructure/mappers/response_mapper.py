from src.application.dtos.response import Response
from httpx import Response as HttpResponse


class ResponseMapper:
    @staticmethod
    async def to_response(response: HttpResponse) -> Response:
        return Response(
            status_code=response.status_code,
            data=response.json(),
            headers=dict(response.headers)
        )
