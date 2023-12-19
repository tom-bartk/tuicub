import pytest
from httperactor import HttpMethod

from src.tuicub.common.state import RemoveCurrentGameroomAction, State
from src.tuicub.common.strings import GAMEROOM_LEAVE_GAMEROOM_CONFIRMATION
from src.tuicub.gameroom.exception import NoCurrentGameroomError
from src.tuicub.gameroom.requests.leave_gameroom import (
    LeaveGameroomInteractor,
    LeaveGameroomRequest,
)


class TestLeaveGameroomRequest:
    @pytest.fixture()
    def sut(self, gameroom_1) -> LeaveGameroomRequest:
        return LeaveGameroomRequest(gameroom=gameroom_1)

    def test_path__returns_gamerooms_gameroom_id_users(
        self, sut: LeaveGameroomRequest, gameroom_id_1
    ) -> None:
        expected = f"/gamerooms/{gameroom_id_1}/users"

        result = sut.path

        assert result == expected

    def test_method__returns_delete(self, sut: LeaveGameroomRequest) -> None:
        expected = HttpMethod.DELETE

        result = sut.method

        assert result == expected


class TestLeaveGameroomInteractor:
    @pytest.fixture()
    def sut(
        self, auth_middleware, confirmation_service, http_client, store
    ) -> LeaveGameroomInteractor:
        return LeaveGameroomInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
        )

    def test_request__when_state_has_no_current_gameroom__raises_no_current_gameroom_error(  # noqa: E501
        self, sut: LeaveGameroomInteractor, store
    ) -> None:
        store.state = State(current_gameroom=None)

        with pytest.raises(NoCurrentGameroomError):
            _ = sut.request

    def test_request__when_state_has_current_gameroom__returns_leave_gameroom_request(
        self, sut: LeaveGameroomInteractor, store, gameroom_1
    ) -> None:
        store.state = State(current_gameroom=gameroom_1)
        expected = LeaveGameroomRequest(gameroom=gameroom_1)

        result = sut.request

        assert result == expected

    def test_actions__returns_remove_current_gameroom_action(
        self, sut: LeaveGameroomInteractor, gameroom_1
    ) -> None:
        expected = [RemoveCurrentGameroomAction()]

        result = sut.actions(response=gameroom_1)

        assert result == expected

    def test_confirmation__returns_leave_gameroom_confirmation(
        self, sut: LeaveGameroomInteractor
    ) -> None:
        expected = GAMEROOM_LEAVE_GAMEROOM_CONFIRMATION

        result = sut.confirmation

        assert result == expected
