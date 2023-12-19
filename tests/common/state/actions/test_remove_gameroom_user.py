import pytest

from src.tuicub.common.models import Gameroom
from src.tuicub.common.state import (
    RemoveGameroomUserAction,
    RemoveGameroomUserReducer,
    State,
)


@pytest.fixture()
def sut() -> RemoveGameroomUserReducer:
    return RemoveGameroomUserReducer()


class TestActionType:
    def test_returns_remove_gameroom_user_action(self, sut) -> None:
        expected = RemoveGameroomUserAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_when_user_in_current_gameroom__returns_state_with_user_removed_from_current_gameroom(  # noqa: E501
        self, sut, gameroom_2, user_1, user_2
    ) -> None:
        expected = State(
            current_gameroom=Gameroom(
                id=gameroom_2.id,
                name=gameroom_2.name,
                owner_id=gameroom_2.owner_id,
                status=gameroom_2.status,
                users=(user_2,),
                game_id=gameroom_2.game_id,
                created_at=gameroom_2.created_at,
            )
        )

        result = sut.apply(
            RemoveGameroomUserAction(user=user_1),
            state=State(current_gameroom=gameroom_2),
        )

        assert result == expected

    def test_when_user_not_in_current_gameroom__does_nothing(
        self, sut, gameroom_3, user_1
    ) -> None:
        expected = State(current_gameroom=gameroom_3)

        result = sut.apply(
            RemoveGameroomUserAction(user=user_1),
            state=State(current_gameroom=gameroom_3),
        )

        assert result == expected
