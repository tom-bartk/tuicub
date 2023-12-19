from unittest.mock import Mock

import pytest

from src.tuicub.game.actions import ResetStateAction
from src.tuicub.game.models import Board
from src.tuicub.game.requests.move import MoveRequest, MoveRequestInteractor
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def board() -> list[list[int]]:
    return [[1, 2, 3], [4, 5, 6]]


class TestMoveRequest:
    def test_game_path__returns_moves(self, game_id, board) -> None:
        sut = MoveRequest(game_id=game_id, board=board)
        expected = "/moves"

        result = sut.game_path

        assert result == expected

    def test_body__returns_board(self, game_id, board) -> None:
        sut = MoveRequest(game_id=game_id, board=board)
        expected = {"board": board}

        result = sut.body

        assert result == expected


class TestMoveRequestInteractor:
    @pytest.fixture()
    def sut(
        self, local_store, auth_middleware, confirmation_service, http_client, store
    ) -> MoveRequestInteractor:
        return MoveRequestInteractor(
            auth=auth_middleware,
            confirmation_service=confirmation_service,
            http_client=http_client,
            store=store,
            local_store=local_store,
        )

    def test_create_request__returns_move_request_with_correct_board(
        self, sut: MoveRequestInteractor, game_id, tileset, tile
    ) -> None:
        board = Board(tilesets=frozenset([tileset(1, 2, 3), tileset(4, 5, 6)]))
        highlighted_tileset = tileset(1, 2, 3)
        selected_tiles = frozenset([tile(4), tile(7), tile(8)])
        state = GameScreenState(
            highlighted_tileset=highlighted_tileset,
            board=board,
            selected_tiles=selected_tiles,
        )
        expected = MoveRequest(game_id=game_id, board=[[5, 6], [1, 2, 3, 4, 7, 8]])

        result = sut.create_request(game_id=game_id, state=state)

        assert result == expected

    @pytest.mark.asyncio()
    async def test_side_effects__dispatches_reset_state_action_to_local_store(
        self, sut: MoveRequestInteractor, local_store
    ) -> None:
        expected = ResetStateAction()

        await sut.side_effects(response=Mock())

        local_store.dispatch.assert_called_once_with(expected)
