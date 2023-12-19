import pytest
from httperactor import HttpMethod

from src.tuicub.game.requests.undo import UndoRequest, UndoRequestInteractor
from src.tuicub.game.state import GameScreenState


class TestUndoRequest:
    def test_game_path__returns_moves(self, game_id) -> None:
        sut = UndoRequest(game_id=game_id)
        expected = "/moves"

        result = sut.game_path

        assert result == expected

    def test_method__returns_delete(self, game_id) -> None:
        sut = UndoRequest(game_id=game_id)
        expected = HttpMethod.DELETE

        result = sut.method

        assert result == expected


class TestUndoRequestInteractor:
    @pytest.fixture()
    def sut(
        self, local_store, auth_middleware, confirmation_service, http_client, store
    ) -> UndoRequestInteractor:
        return UndoRequestInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
            local_store=local_store,
        )

    def test_create_request__returns_undo_request_w_game_id(
        self, sut: UndoRequestInteractor, game_id
    ) -> None:
        expected = UndoRequest(game_id=game_id)

        result = sut.create_request(game_id=game_id, state=GameScreenState())

        assert result == expected
