import pytest

from src.tuicub.game.requests.end_turn import EndTurnRequest, EndTurnRequestInteractor
from src.tuicub.game.state import GameScreenState


class TestEndTurnRequest:
    __slots__ = ()

    def test_game_path__returns_turns_end(self, game_id) -> None:
        sut = EndTurnRequest(game_id=game_id)
        expected = "/turns/end"

        result = sut.game_path

        assert result == expected


class TestEndTurnRequestInteractor:
    __slots__ = ()

    @pytest.fixture()
    def sut(
        self, local_store, auth_middleware, confirmation_service, http_client, store
    ) -> EndTurnRequestInteractor:
        return EndTurnRequestInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
            local_store=local_store,
        )

    def test_create_request__returns_end_turn_request_w_game_id(
        self, sut: EndTurnRequestInteractor, game_id
    ) -> None:
        expected = EndTurnRequest(game_id=game_id)

        result = sut.create_request(game_id=game_id, state=GameScreenState())

        assert result == expected
