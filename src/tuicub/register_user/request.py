import json
from collections.abc import Sequence
from typing import Any

import httpx
from asockit import SocketWriter
from attrs import frozen
from httperactor import AuthMiddleware, HttpMethod, Request
from marshmallow_generic import GenericSchema, fields
from pydepot import Action, Store

from ..common.http import BaseHttpInteractor, BaseRequest
from ..common.models import User
from ..common.schemas import UserSchema
from ..common.services.auth_service import AuthService
from ..common.state import SetCurrentUserAction
from .state import RegisterUserState


@frozen
class RegisterUserResponse:
    """The response of the register user request.

    Attributes:
        token (str): The authentication token of the registered user.
        user (User): The registered user.
    """

    token: str
    user: User


class RegisterUserRequest(BaseRequest[RegisterUserResponse]):
    """The request for registering a new user.

    Request documentation: https://docs.tuicub.com/api/#/Users/register_user
    """

    __slots__ = ("_name",)

    def __init__(self, name: str):
        """Initialize new request.

        Args:
            name (str): The name of the user to send.
        """
        self._name: str = name

    @property
    def path(self) -> str:
        return "/users"

    @property
    def method(self) -> HttpMethod:
        return HttpMethod.POST

    @property
    def body(self) -> list | dict | None:
        return {"name": self._name}

    @property
    def response_schema(self) -> GenericSchema[RegisterUserResponse]:
        return RegisterUserResponseSchema()


class RegisterUserInteractor(BaseHttpInteractor[RegisterUserResponse]):
    """The interactor for sending the register user request."""

    __slots__ = ("_auth_service", "_socket_writer", "_local_store")

    def __init__(
        self,
        auth_service: AuthService,
        socket_writer: SocketWriter,
        local_store: Store[RegisterUserState],
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize new interactor.

        Args:
            auth_service (AuthService): The service that stores the authentication token.
            socket_writer (SocketWriter): The writable connection to the events server.
            local_store (Store[RegisterUserState]): The local screen store.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self._auth_service: AuthService = auth_service
        self._socket_writer: SocketWriter = socket_writer
        self._local_store: Store[RegisterUserState] = local_store

    @property
    def request(self) -> Request[RegisterUserResponse]:
        return RegisterUserRequest(name=self._local_store.state.name)

    @property
    def auth(self) -> AuthMiddleware[httpx.Request] | None:
        return None

    def actions(self, response: RegisterUserResponse) -> Sequence[Action]:
        """Actions to dispatch for the register user response.

        Dispatches a `SetCurrentUserAction` with the registered user.

        Args:
            response (RegisterUserResponse): The register user response.

        Returns:
            A list of actions to dispatch.
        """
        return [SetCurrentUserAction(user=response.user)]

    async def side_effects(self, response: RegisterUserResponse) -> None:
        """Side effects for the register user request.

        Stores the authentication token in the auth service. Then, writes the
        connect request to the events server with the new token.

        Args:
            response (RegisterUserResponse): The register user response.
        """
        self._auth_service.save_token(token=response.token)
        await self._socket_writer.write(json.dumps({"token": response.token}))


class RegisterUserResponseSchema(GenericSchema[RegisterUserResponse]):
    """The schema for the register user response."""

    token = fields.Str()
    user = fields.Nested(UserSchema)
