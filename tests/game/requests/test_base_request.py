from typing import Any
from unittest.mock import Mock

import pytest
from httperactor import HttpMethod

from src.tuicub.common.schemas import GameStateSchema
from src.tuicub.game.requests.base import GameRequest


class DummyGameRequest(GameRequest):
    __slots__ = ("mock_game_path",)

    def __init__(self, *args: Any, **kwargs: Any):
        self.mock_game_path = Mock()
        super().__init__(*args, **kwargs)

    @property
    def game_path(self) -> str:
        return self.mock_game_path()


@pytest.fixture()
def sut(game_id) -> DummyGameRequest:
    return DummyGameRequest(game_id=game_id)


class TestRequest:
    def test_path__returns_games_game_id_game_path(self, sut, game_id) -> None:
        sut.mock_game_path.return_value = "/foo"
        expected = f"/games/{game_id}/foo"

        result = sut.path

        assert result == expected

    def test_method__returns_post(self, sut) -> None:
        expected = HttpMethod.POST

        result = sut.method

        assert result == expected

    def test_response_schema__returns_game_state_schema(self, sut) -> None:
        result = sut.response_schema

        assert isinstance(result, GameStateSchema)
