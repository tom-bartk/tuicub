import pytest
from httperactor import HttpMethod

from src.tuicub.game.requests.redo import RedoRequest, RedoRequestInteractor
from src.tuicub.game.state import GameScreenState


class TestRedoRequest:
    def test_game_path__returns_moves(self, game_id) -> None:
        sut = RedoRequest(game_id=game_id)
        expected = "/moves"

        result = sut.game_path

        assert result == expected

    def test_method__returns_patch(self, game_id) -> None:
        sut = RedoRequest(game_id=game_id)
        expected = HttpMethod.PATCH

        result = sut.method

        assert result == expected


class TestRedoRequestInteractor:
    @pytest.fixture()
    def sut(
        self, local_store, auth_middleware, confirmation_service, http_client, store
    ) -> RedoRequestInteractor:
        return RedoRequestInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
            local_store=local_store,
        )

    def test_create_request__returns_redo_request_w_game_id(
        self, sut: RedoRequestInteractor, game_id
    ) -> None:
        expected = RedoRequest(game_id=game_id)

        result = sut.create_request(game_id=game_id, state=GameScreenState())

        assert result == expected
