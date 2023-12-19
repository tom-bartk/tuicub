import pytest
from httperactor import HttpMethod

from src.tuicub.common.state import DeleteGameroomAction, State
from src.tuicub.common.strings import GAMEROOM_DELETE_GAMEROOM_CONFIRMATION
from src.tuicub.gameroom.exception import NoCurrentGameroomError
from src.tuicub.gameroom.requests.delete_gameroom import (
    DeleteGameroomInteractor,
    DeleteGameroomRequest,
)


class TestDeleteGameroomRequest:
    @pytest.fixture()
    def sut(self, gameroom_1) -> DeleteGameroomRequest:
        return DeleteGameroomRequest(gameroom=gameroom_1)

    def test_path__returns_gamerooms_gameroom_id(
        self, sut: DeleteGameroomRequest, gameroom_id_1
    ) -> None:
        expected = f"/gamerooms/{gameroom_id_1}"

        result = sut.path

        assert result == expected

    def test_method__returns_delete(self, sut: DeleteGameroomRequest) -> None:
        expected = HttpMethod.DELETE

        result = sut.method

        assert result == expected


class TestDeleteGameroomInteractor:
    @pytest.fixture()
    def sut(
        self, auth_middleware, confirmation_service, http_client, store
    ) -> DeleteGameroomInteractor:
        return DeleteGameroomInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
        )

    def test_request__when_state_has_no_current_gameroom__raises_no_current_gameroom_error(  # noqa: E501
        self, sut: DeleteGameroomInteractor, store
    ) -> None:
        store.state = State(current_gameroom=None)

        with pytest.raises(NoCurrentGameroomError):
            _ = sut.request

    def test_request__when_state_has_current_gameroom__returns_delete_gameroom_request(
        self, sut: DeleteGameroomInteractor, store, gameroom_1
    ) -> None:
        store.state = State(current_gameroom=gameroom_1)
        expected = DeleteGameroomRequest(gameroom=gameroom_1)

        result = sut.request

        assert result == expected

    def test_actions__returns_delete_gameroom_action_with_response_gameroom(
        self, sut: DeleteGameroomInteractor, gameroom_1
    ) -> None:
        expected = [DeleteGameroomAction(gameroom=gameroom_1)]

        result = sut.actions(response=gameroom_1)

        assert result == expected

    def test_confirmation__returns_delete_gameroom_confirmation(
        self, sut: DeleteGameroomInteractor
    ) -> None:
        expected = GAMEROOM_DELETE_GAMEROOM_CONFIRMATION

        result = sut.confirmation

        assert result == expected
