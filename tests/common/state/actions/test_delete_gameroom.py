import pytest

from src.tuicub.common.state import DeleteGameroomAction, DeleteGameroomReducer, State


@pytest.fixture()
def sut() -> DeleteGameroomReducer:
    return DeleteGameroomReducer()


class TestActionType:
    def test_returns_delete_gameroom_action(self, sut) -> None:
        expected = DeleteGameroomAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_when_gameroom_is_current_gameroom__returns_state_with_none_current_gameroom(
        self, sut, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        expected = State(current_gameroom=None, gamerooms=(gameroom_1, gameroom_2))

        result = sut.apply(
            DeleteGameroomAction(gameroom=gameroom_3),
            state=State(
                current_gameroom=gameroom_3,
                gamerooms=(gameroom_1, gameroom_2, gameroom_3),
            ),
        )

        assert result == expected

    def test_returns_state_without_gameroom(
        self, sut, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        expected = State(gamerooms=(gameroom_1, gameroom_2))

        result = sut.apply(
            DeleteGameroomAction(gameroom=gameroom_3),
            state=State(gamerooms=(gameroom_1, gameroom_2, gameroom_3)),
        )

        assert result == expected
