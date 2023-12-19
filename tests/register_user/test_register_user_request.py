from unittest.mock import create_autospec

import pytest
from httperactor import HttpMethod
from pydepot import Store

from src.tuicub.common.state import SetCurrentUserAction
from src.tuicub.register_user.request import (
    RegisterUserInteractor,
    RegisterUserRequest,
    RegisterUserResponse,
    RegisterUserResponseSchema,
)
from src.tuicub.register_user.state import RegisterUserState


@pytest.fixture()
def name() -> str:
    return "foo"


@pytest.fixture()
def local_store() -> Store[RegisterUserState]:
    return create_autospec(Store)


class TestRegisterUserRequest:
    @pytest.fixture()
    def sut(self, name) -> RegisterUserRequest:
        return RegisterUserRequest(name=name)

    def test_path__returns_users(self, sut: RegisterUserRequest) -> None:
        expected = "/users"

        result = sut.path

        assert result == expected

    def test_method__returns_post(self, sut: RegisterUserRequest) -> None:
        expected = HttpMethod.POST

        result = sut.method

        assert result == expected

    def test_body__returns_dict_with_name(self, sut: RegisterUserRequest, name) -> None:
        expected = {"name": name}

        result = sut.body

        assert result == expected

    def test_response_schema__returns_register_user_response_schema(
        self, sut: RegisterUserRequest
    ) -> None:
        result = sut.response_schema

        assert isinstance(result, RegisterUserResponseSchema)


class TestRegisterUserInteractor:
    @pytest.fixture()
    def sut(
        self,
        auth_service,
        socket_writer,
        auth_middleware,
        confirmation_service,
        http_client,
        store,
        local_store,
    ) -> RegisterUserInteractor:
        return RegisterUserInteractor(
            auth_service=auth_service,
            socket_writer=socket_writer,
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
            local_store=local_store,
        )

    def test_request__returns_register_user_request_with_name_from_local_store(
        self, sut: RegisterUserInteractor, local_store, name
    ) -> None:
        local_store.state = RegisterUserState(name=name)
        expected = RegisterUserRequest(name=name)

        result = sut.request

        assert result == expected

    def test_auth__does_not_require_authentication(
        self, sut: RegisterUserInteractor
    ) -> None:
        expected = None

        result = sut.auth

        assert result == expected

    def test_actions__returns_set_current_user_action_with_response_user(
        self, sut: RegisterUserInteractor, user_1
    ) -> None:
        expected = [SetCurrentUserAction(user=user_1)]

        result = sut.actions(response=RegisterUserResponse(token="token", user=user_1))

        assert result == expected

    @pytest.mark.asyncio()
    async def test_side_effects__saves_token_from_response(
        self, sut: RegisterUserInteractor, auth_service, user_1
    ) -> None:
        await sut.side_effects(response=RegisterUserResponse(token="token", user=user_1))

        auth_service.save_token.assert_called_once_with(token="token")

    @pytest.mark.asyncio()
    async def test_side_effects__sends_connect_request_to_events_server(
        self, sut: RegisterUserInteractor, auth_service, user_1, socket_writer
    ) -> None:
        await sut.side_effects(response=RegisterUserResponse(token="token", user=user_1))

        socket_writer.write.assert_awaited_once_with('{"token": "token"}')
