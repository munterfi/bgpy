from .environment import ENV_TOKEN
from os import environ
from secrets import token_urlsafe
from typing import Optional


def token_create(length: int = 64) -> str:
    """
    Creates a url safe token with a defined length.

    Parameters
    ----------
    length : int, optional
        Length of the token, by default 64

    Returns
    -------
    str
        The token.
    """
    return token_urlsafe(length)


def token_setenv(token: Optional[str]) -> None:
    """
    Sets a token in the environment.

    Parameters
    ----------
    token : Optional[str]
        The token to set.
    """
    if token is not None:
        environ[ENV_TOKEN] = token


def token_getenv() -> Optional[str]:
    """
    Gets the token from the environment.

    Returns
    -------
    Optional[str]
        The token.
    """
    try:
        return environ[ENV_TOKEN]
    except KeyError:
        return None


def token_delenv() -> None:
    """
    Deletes the token from the environment.
    """
    try:
        del environ[ENV_TOKEN]
    except KeyError:
        pass
