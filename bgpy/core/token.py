from .environment import ENV_TOKEN
from os import environ
from secrets import token_urlsafe
from typing import Optional


def token_create(length: int = 64) -> str:
    return token_urlsafe(length)


def token_setenv(token: Optional[str]) -> None:
    if token is not None:
        environ[ENV_TOKEN] = token


def token_getenv() -> Optional[str]:
    try:
        return environ[ENV_TOKEN]
    except KeyError:
        return None


def token_delenv() -> None:
    try:
        del environ[ENV_TOKEN]
    except KeyError:
        pass
