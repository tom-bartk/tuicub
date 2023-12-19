import pytest
from httperactor import HttpMethod

from src.tuicub.common.schemas import GameSchema
from src.tuicub.common.state import SetCurrentGameAction, State
from src.tuicub.common.strings import GAMEROOM_START_GAME_CONFIRMATION
from src.tuicub.gameroom.exception import NoCurrentGameroomError
from src.tuicub.gameroom.requests.start_game import StartGameInteractor, StartGameRequest


class TestStartGameRequest:
    @pytest.fixture()
    def sut(self, gameroom_1) -> StartGameRequest:
        return StartGameRequest(gameroom=gameroom_1)

    def test_path__returns_gamerooms_gameroom_id_game(
        self, sut: StartGameRequest, gameroom_id_1
    ) -> None:
        expected = f"/gamerooms/{gameroom_id_1}/game"

        result = sut.path

        assert result == expected

    def test_method__returns_post(self, sut: StartGameRequest) -> None:
        expected = HttpMethod.POST

        result = sut.method

        assert result == expected

    def test_response_schema__returns_game_schema(self, sut: StartGameRequest) -> None:
        result = sut.response_schema

        assert isinstance(result, GameSchema)


class TestStartGameInteractor:
    @pytest.fixture()
    def sut(
        self, auth_middleware, confirmation_service, http_client, store
    ) -> StartGameInteractor:
        return StartGameInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
        )

    def test_request__when_state_has_no_current_gameroom__raises_no_current_gameroom_error(  # noqa: E501
        self, sut: StartGameInteractor, store
    ) -> None:
        store.state = State(current_gameroom=None)

        with pytest.raises(NoCurrentGameroomError):
            _ = sut.request

    def test_request__when_state_has_current_gameroom__returns_start_game_request(
        self, sut: StartGameInteractor, store, gameroom_1
    ) -> None:
        store.state = State(current_gameroom=gameroom_1)
        expected = StartGameRequest(gameroom=gameroom_1)

        result = sut.request

        assert result == expected

    def test_actions__returns_set_current_game_action_with_game_from_response(
        self, sut: StartGameInteractor, game
    ) -> None:
        expected = [SetCurrentGameAction(game=game)]

        result = sut.actions(response=game)

        assert result == expected

    def test_confirmation__returns_start_game_confirmation(
        self, sut: StartGameInteractor
    ) -> None:
        expected = GAMEROOM_START_GAME_CONFIRMATION

        result = sut.confirmation

        assert result == expected
