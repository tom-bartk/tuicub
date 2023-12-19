from unittest.mock import Mock

import pytest
from httperactor import HttpMethod

from src.tuicub.common.schemas import GameroomSchema
from src.tuicub.common.state import SetCurrentGameroomAction
from src.tuicub.gamerooms.requests.create_gameroom import (
    CreateGameroomInteractor,
    CreateGameroomRequest,
)


class TestCreateGameroomRequest:
    @pytest.fixture()
    def sut(self) -> CreateGameroomRequest:
        return CreateGameroomRequest()

    def test_path__returns_gamerooms(self, sut: CreateGameroomRequest) -> None:
        expected = "/gamerooms"

        result = sut.path

        assert result == expected

    def test_method__returns_post(self, sut: CreateGameroomRequest) -> None:
        expected = HttpMethod.POST

        result = sut.method

        assert result == expected

    def test_response_schema__returns_gameroom_schema(
        self, sut: CreateGameroomRequest
    ) -> None:
        result = sut.response_schema

        assert isinstance(result, GameroomSchema)


class TestCreateGameroomInteractor:
    @pytest.fixture()
    def sut(
        self, auth_middleware, confirmation_service, http_client, store
    ) -> CreateGameroomInteractor:
        return CreateGameroomInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
        )

    def test_request__returns_create_gameroom_request(
        self, sut: CreateGameroomInteractor
    ) -> None:
        expected = CreateGameroomRequest()

        result = sut.request

        assert result == expected

    def test_actions__returns_set_current_gameroom_action_with_response_gameroom(
        self, sut: CreateGameroomInteractor
    ) -> None:
        gameroom = Mock()
        expected = [SetCurrentGameroomAction(gameroom=gameroom)]

        result = sut.actions(response=gameroom)

        assert result == expected
