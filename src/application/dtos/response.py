from typing import Generic, TypeVar, Any, Dict, Tuple

T = TypeVar('T')


class Response(Generic[T]):
    __slots__: Tuple[str, ...] = ("status_code", "data", "headers",)

    def __init__(self, status_code: int, data: Any, headers: Dict[str, str]):
        self.status_code: int = status_code
        self.data: Any = data
        self.headers: Dict[str, str] = headers
