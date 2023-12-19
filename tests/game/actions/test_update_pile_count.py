import pytest

from src.tuicub.game.actions import UpdatePileCountAction, UpdatePileCountReducer
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> UpdatePileCountReducer:
    return UpdatePileCountReducer()


class TestActionType:
    def test_returns_update_pile_count_action(self, sut) -> None:
        expected = UpdatePileCountAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_new_pile_count(self, sut) -> None:
        current = GameScreenState(pile_count=13)
        expected = GameScreenState(pile_count=42)

        result = sut.apply(UpdatePileCountAction(pile_count=42), state=current)

        assert result == expected
