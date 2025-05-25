from typing import Literal
from dataclasses import dataclass


@dataclass(slots=True)
class JWTData:
    secret_key: str
    algorithm: str
    expire: int


@dataclass(slots=True)
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str
    database: str


@dataclass(slots=True)
class Config:
    debug: bool
    log_level: Literal["debug", "info", "warning", "error", "critical"]
    database: DatabaseConfig
    jwt: JWTData
