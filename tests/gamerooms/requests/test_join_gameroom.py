from unittest.mock import Mock

import pytest
from httperactor import HttpMethod

from src.tuicub.common.state import SetCurrentGameroomAction, State
from src.tuicub.gamerooms.requests.join_gameroom import (
    GameroomNotSelectedError,
    JoinGameroomInteractor,
    JoinGameroomRequest,
)
from src.tuicub.gamerooms.state import GameroomsState


class TestJoinGameroomRequest:
    @pytest.fixture()
    def sut(self, gameroom_1) -> JoinGameroomRequest:
        return JoinGameroomRequest(gameroom=gameroom_1)

    def test_path__returns_gamerooms_gameroom_id_users(
        self, sut: JoinGameroomRequest, gameroom_id_1
    ) -> None:
        expected = f"/gamerooms/{gameroom_id_1}/users"

        result = sut.path

        assert result == expected

    def test_method__returns_post(self, sut: JoinGameroomRequest) -> None:
        expected = HttpMethod.POST

        result = sut.method

        assert result == expected


class TestJoinGameroomInteractor:
    @pytest.fixture()
    def sut(
        self, auth_middleware, confirmation_service, http_client, store, local_store
    ) -> JoinGameroomInteractor:
        return JoinGameroomInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
            local_store=local_store,
        )

    def test_request__when_global_store_has_no_gamerooms__raises_gameroom_not_selected_error(  # noqa: E501
        self, sut: JoinGameroomInteractor, store
    ) -> None:
        store.state = State(gamerooms=())

        with pytest.raises(GameroomNotSelectedError):
            _ = sut.request

    def test_request__when_local_selected_index_gte_global_gamerooms_len__raises_gameroom_not_selected_error(  # noqa: E501
        self, sut: JoinGameroomInteractor, store, local_store
    ) -> None:
        local_store.state = GameroomsState(selected_index=2)
        store.state = State(gamerooms=(Mock(), Mock()))

        with pytest.raises(GameroomNotSelectedError):
            _ = sut.request

    def test_request__when_local_selected_index_lt_global_gamerooms_len__returns_join_gameroom_request(  # noqa: E501
        self, sut: JoinGameroomInteractor, store, local_store, gameroom_1, gameroom_2
    ) -> None:
        local_store.state = GameroomsState(selected_index=1)
        store.state = State(gamerooms=(gameroom_1, gameroom_2))
        expected = JoinGameroomRequest(gameroom=gameroom_2)

        result = sut.request

        assert result == expected

    def test_actions__returns_set_current_gameroom_action_with_response_gameroom(
        self, sut: JoinGameroomInteractor, gameroom_1
    ) -> None:
        expected = [SetCurrentGameroomAction(gameroom=gameroom_1)]

        result = sut.actions(response=gameroom_1)

        assert result == expected
