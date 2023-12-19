import pytest

from src.tuicub.game.requests.draw import DrawRequest, DrawRequestInteractor
from src.tuicub.game.state import GameScreenState


class TestDrawRequest:
    def test_game_path__returns_turns_draw(self, game_id) -> None:
        sut = DrawRequest(game_id=game_id)
        expected = "/turns/draw"

        result = sut.game_path

        assert result == expected


class TestDrawRequestInteractor:
    @pytest.fixture()
    def sut(
        self, local_store, auth_middleware, confirmation_service, http_client, store
    ) -> DrawRequestInteractor:
        return DrawRequestInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
            local_store=local_store,
        )

    def test_create_request__returns_draw_request_w_game_id(
        self, sut: DrawRequestInteractor, game_id
    ) -> None:
        expected = DrawRequest(game_id=game_id)

        result = sut.create_request(game_id=game_id, state=GameScreenState())

        assert result == expected
