from typing import Any
from unittest.mock import Mock

import pytest
from httperactor import Request

from src.tuicub.common.models import GameState
from src.tuicub.common.state import State
from src.tuicub.game.errors import NoCurrentGameError
from src.tuicub.game.requests.base import BaseGameRequestInteractor
from src.tuicub.game.state import GameScreenState


class DummyBaseGameRequestInteractor(BaseGameRequestInteractor):
    __slots__ = ("mock_create_request",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.mock_create_request = Mock()
        super().__init__(*args, **kwargs)

    def create_request(self, game_id: str, state: GameScreenState) -> Request[GameState]:
        return self.mock_create_request(game_id=game_id, state=state)


@pytest.fixture()
def sut(
    local_store, auth_middleware, confirmation_service, http_client, store
) -> DummyBaseGameRequestInteractor:
    return DummyBaseGameRequestInteractor(
        auth=auth_middleware,
        confirmation_service=confirmation_service,
        http_client=http_client,
        store=store,
        local_store=local_store,
    )


class TestRequest:
    def test_when_global_state_has_no_current_game__raises_no_current_game_error(
        self, sut, store
    ) -> None:
        store.state = State(current_game=None)

        with pytest.raises(NoCurrentGameError):
            _ = sut.request

    def test_when_global_state_has_current_game__returns_result_of_create_request(
        self, sut, store, local_store
    ) -> None:
        game = Mock()
        game.id = "foo"
        store.state = State(current_game=game)
        local_store.state = GameScreenState()
        expected = Mock()
        sut.mock_create_request.return_value = expected

        result = sut.request

        assert result == expected
        sut.mock_create_request.assert_called_once_with(
            game_id="foo", state=GameScreenState()
        )


class TestActions:
    def test_returns_empty_list(self, sut) -> None:
        expected: list = []

        result = sut.actions(response=Mock())

        assert result == expected
