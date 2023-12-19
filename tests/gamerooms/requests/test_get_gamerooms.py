from unittest.mock import Mock

import pytest

from src.tuicub.common.schemas import GameroomSchema
from src.tuicub.common.state import SetGameroomsAction
from src.tuicub.gamerooms.requests.get_gamerooms import (
    GetGameroomsInteractor,
    GetGameroomsRequest,
)


class TestGetGameroomsRequest:
    @pytest.fixture()
    def sut(self) -> GetGameroomsRequest:
        return GetGameroomsRequest()

    def test_path__returns_gamerooms(self, sut: GetGameroomsRequest) -> None:
        expected = "/gamerooms"

        result = sut.path

        assert result == expected

    def test_returns_list__returns_true(self, sut: GetGameroomsRequest) -> None:
        expected = True

        result = sut.returns_list

        assert result == expected

    def test_response_schema__returns_gameroom_schema(
        self, sut: GetGameroomsRequest
    ) -> None:
        result = sut.response_schema

        assert isinstance(result, GameroomSchema)


class TestGetGameroomsInteractor:
    @pytest.fixture()
    def sut(
        self, auth_middleware, confirmation_service, http_client, store
    ) -> GetGameroomsInteractor:
        return GetGameroomsInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
        )

    def test_request__returns_get_gamerooms_request(
        self, sut: GetGameroomsInteractor
    ) -> None:
        expected = GetGameroomsRequest()

        result = sut.request

        assert result == expected

    def test_actions__returns_set_gamerooms_action_with_response_gamerooms(
        self, sut: GetGameroomsInteractor
    ) -> None:
        gamerooms = [Mock(), Mock()]
        expected = [SetGameroomsAction(gamerooms=gamerooms)]

        result = sut.actions(response=gamerooms)

        assert result == expected
