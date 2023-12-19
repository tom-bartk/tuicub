import pytest

from src.tuicub.game.actions import UpdateRackAction, UpdateRackReducer
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> UpdateRackReducer:
    return UpdateRackReducer()


class TestActionType:
    def test_returns_update_rack_action(self, sut) -> None:
        expected = UpdateRackAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_new_rack(self, sut, tileset) -> None:
        current = GameScreenState(rack=tileset(1, 2, 3))
        expected = GameScreenState(rack=tileset(4, 5, 6))

        result = sut.apply(UpdateRackAction(rack=tileset(4, 5, 6)), state=current)

        assert result == expected
