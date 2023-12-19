import pytest

from src.tuicub.common.state import SetGameroomsAction, SetGameroomsReducer, State


@pytest.fixture()
def sut() -> SetGameroomsReducer:
    return SetGameroomsReducer()


class TestActionType:
    def test_returns_set_gamerooms_action(self, sut) -> None:
        expected = SetGameroomsAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_updated_gamerooms(
        self, sut, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        expected = State(gamerooms=(gameroom_1, gameroom_2, gameroom_3))

        result = sut.apply(
            SetGameroomsAction(gamerooms=(gameroom_1, gameroom_2, gameroom_3)),
            state=State(gamerooms=()),
        )

        assert result == expected
