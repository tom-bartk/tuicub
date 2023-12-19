from typing import Any, Generic, TypeVar

import httpx
from httperactor import AuthMiddleware, HttpInteractor

from ..confirmation import ConfirmationService
from ..state import State
from .auth_middleware import BearerTokenAuthMiddleware

TResponse = TypeVar("TResponse")


class BaseHttpInteractor(
    Generic[TResponse], HttpInteractor[httpx.Request, TResponse, State]
):
    """Base class for an http interactor."""

    __slots__ = ("_auth", "_confirmation_service")

    def __init__(
        self,
        auth: BearerTokenAuthMiddleware,
        confirmation_service: ConfirmationService,
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize new interactor.

        Args:
            auth (BearerTokenAuthMiddleware): The auth middlware.
            confirmation_service (ConfirmationService): The confirmation service.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.
        """
        self._auth: BearerTokenAuthMiddleware = auth
        self._confirmation_service: ConfirmationService = confirmation_service
        super().__init__(*args, **kwargs)

    @property
    def auth(self) -> AuthMiddleware[httpx.Request] | None:
        return self._auth

    @property
    def confirmation(self) -> str:
        return ""

    async def execute(self) -> None:
        """Execute the request.

        If the confirmation text is not empty and the confirmation is rejected,
        the request is not sent. Otherwise, the request is sent normally.
        """
        if self.confirmation:
            answer = await self._confirmation_service.confirm(self.confirmation)
            if not answer:
                return
        await super().execute()
