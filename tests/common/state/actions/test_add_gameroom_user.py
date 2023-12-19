import pytest

from src.tuicub.common.models import Gameroom
from src.tuicub.common.state import AddGameroomUserAction, AddGameroomUserReducer, State


@pytest.fixture()
def sut() -> AddGameroomUserReducer:
    return AddGameroomUserReducer()


class TestActionType:
    def test_returns_add_gameroom_user_action(self, sut) -> None:
        expected = AddGameroomUserAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_when_user_not_in_current_gameroom__returns_state_with_user_added_to_current_gameroom(  # noqa: E501
        self, sut, gameroom_3, user_1, user_3
    ) -> None:
        expected = State(
            current_gameroom=Gameroom(
                id=gameroom_3.id,
                name=gameroom_3.name,
                owner_id=gameroom_3.owner_id,
                status=gameroom_3.status,
                users=(user_3, user_1),
                game_id=gameroom_3.game_id,
                created_at=gameroom_3.created_at,
            )
        )

        result = sut.apply(
            AddGameroomUserAction(user=user_1), state=State(current_gameroom=gameroom_3)
        )

        assert result == expected

    def test_when_user_in_current_gameroom__does_nothing(
        self, sut, gameroom_3, user_3
    ) -> None:
        expected = State(current_gameroom=gameroom_3)

        result = sut.apply(
            AddGameroomUserAction(user=user_3), state=State(current_gameroom=gameroom_3)
        )

        assert result == expected
