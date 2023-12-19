import pytest

from src.tuicub.common.events.factory import EventSchemas, TuicubEventsFactory
from src.tuicub.common.models import (
    Game,
    Gameroom,
    GameroomStatus,
    GameState,
    Player,
    User,
)
from src.tuicub.common.schemas import TuicubEventSchema
from src.tuicub.game.events import (
    BoardChangedEvent,
    BoardChangedEventSchema,
    PileCountChangedEvent,
    PileCountChangedEventSchema,
    PlayerLeftEvent,
    PlayerLeftEventSchema,
    PlayersChangedEvent,
    PlayersChangedEventSchema,
    PlayerWonEvent,
    PlayerWonEventSchema,
    RackChangedEvent,
    RackChangedEventSchema,
    TileDrawnEvent,
    TileDrawnEventSchema,
    TurnEndedEvent,
    TurnStartedEvent,
)
from src.tuicub.gameroom.events import (
    GameroomDeletedEvent,
    GameroomDeletedEventSchema,
    GameStartedEvent,
    GameStartedEventSchema,
    UserJoinedEvent,
    UserJoinedEventSchema,
    UserLeftEvent,
    UserLeftEventSchema,
)


@pytest.fixture()
def schemas() -> EventSchemas:
    return EventSchemas(
        base_schema=TuicubEventSchema(),
        board_changed=BoardChangedEventSchema(),
        game_started=GameStartedEventSchema(),
        gameroom_deleted=GameroomDeletedEventSchema(),
        pile_count_changed=PileCountChangedEventSchema(),
        player_left=PlayerLeftEventSchema(),
        player_won=PlayerWonEventSchema(),
        players_changed=PlayersChangedEventSchema(),
        rack_changed=RackChangedEventSchema(),
        tile_drawn=TileDrawnEventSchema(),
        user_joined=UserJoinedEventSchema(),
        user_left=UserLeftEventSchema(),
    )


@pytest.fixture()
def sut(schemas) -> TuicubEventsFactory:
    return TuicubEventsFactory(event_schemas=schemas)


class TestCreate:
    def test_when_event_board_changed__returns_board_changed_event(self, sut) -> None:
        raw = (
            '{"name": "board_changed", "data": '
            '{"board": [[1, 2, 3], [4, 5, 6]], "new_tiles": [1, 4]}}'
        )
        expected = BoardChangedEvent(board=[[1, 2, 3], [4, 5, 6]], new_tiles=[1, 4])

        result = sut.create(raw)

        assert result == expected

    def test_when_event_game_started__returns_game_started_event(self, sut) -> None:
        raw = (
            '{"name": "game_started", "data": {"game": '
            '{"id": "foo", "gameroom_id": "bar", "winner": null, "game_state": '
            '{"players": ['
            '{"name": "Alice", "user_id": "123", "tiles_count": 42, "has_turn": false},'
            '{"name": "Bob", "user_id": "456", "tiles_count": 13, "has_turn": true}'
            "],"
            '"board": [[1, 2, 3], [4, 5, 6]], "pile_count": 7, "rack": [7, 8, 9]}}}}'
        )
        game = Game(
            id="foo",
            gameroom_id="bar",
            winner=None,
            game_state=GameState(
                players=[
                    Player(user_id="123", tiles_count=42, has_turn=False, name="Alice"),
                    Player(user_id="456", name="Bob", tiles_count=13, has_turn=True),
                ],
                board=[[1, 2, 3], [4, 5, 6]],
                pile_count=7,
                rack=[7, 8, 9],
            ),
        )
        expected = GameStartedEvent(game=game)

        result = sut.create(raw)

        assert result == expected

    def test_when_event_gameroom_deleted__returns_gameroom_deleted_event(
        self, sut
    ) -> None:
        raw = (
            '{"name": "gameroom_deleted", "data": {"gameroom": '
            '{"id": "foo", "game_id": null, "name": "bar", "owner_id": "baz", '
            '"status": "STARTING", "created_at": 1698397784856.701, "users": ['
            '{"name": "Alice", "id": "123"},'
            '{"name": "Bob", "id": "456"}'
            "]}}}"
        )
        gameroom = Gameroom(
            id="foo",
            name="bar",
            owner_id="baz",
            game_id=None,
            status=GameroomStatus.STARTING,
            users=(
                User(id="123", name="Alice"),
                User(id="456", name="Bob"),
            ),
        )
        expected = GameroomDeletedEvent(gameroom=gameroom)

        result = sut.create(raw)

        assert result == expected

    def test_when_event_pile_count_changed__returns_pile_count_changed_event(
        self, sut
    ) -> None:
        raw = '{"name": "pile_count_changed", "data": {"pile_count": 42}}'

        expected = PileCountChangedEvent(pile_count=42)

        result = sut.create(raw)

        assert result == expected

    def test_when_event_player_left__returns_player_left_event(self, sut) -> None:
        raw = (
            '{"name": "player_left", "data": {"player": '
            '{"name": "Alice", "user_id": "123", "tiles_count": 42, "has_turn": false}'
            "}}"
        )
        expected = PlayerLeftEvent(
            player=Player(user_id="123", tiles_count=42, has_turn=False, name="Alice")
        )

        result = sut.create(raw)

        assert result == expected

    def test_when_event_player_won__returns_player_won_event(self, sut) -> None:
        raw = (
            '{"name": "player_won", "data": {"winner": '
            '{"name": "Alice", "user_id": "123", "tiles_count": 42, "has_turn": false}'
            "}}"
        )
        expected = PlayerWonEvent(
            winner=Player(user_id="123", tiles_count=42, has_turn=False, name="Alice")
        )

        result = sut.create(raw)

        assert result == expected

    def test_when_event_players_changed__returns_players_changed_event(self, sut) -> None:
        raw = (
            '{"name": "players_changed", "data": {"players": ['
            '{"name": "Alice", "user_id": "123", "tiles_count": 42, "has_turn": false},'
            '{"name": "Bob", "user_id": "456", "tiles_count": 13, "has_turn": true}'
            "]}}"
        )
        expected = PlayersChangedEvent(
            players=[
                Player(user_id="123", tiles_count=42, has_turn=False, name="Alice"),
                Player(user_id="456", name="Bob", tiles_count=13, has_turn=True),
            ]
        )

        result = sut.create(raw)

        assert result == expected

    def test_when_event_rack_changed__returns_rack_changed_event(self, sut) -> None:
        raw = '{"name": "rack_changed", "data": {"rack": [1, 2, 3]}}'
        expected = RackChangedEvent(rack=[1, 2, 3])

        result = sut.create(raw)

        assert result == expected

    def test_when_event_tile_drawn__returns_tile_drawn_event(self, sut) -> None:
        raw = '{"name": "tile_drawn", "data": {"tile": 1}}'
        expected = TileDrawnEvent(tile=1)

        result = sut.create(raw)

        assert result == expected

    def test_when_event_turn_ended__returns_turn_ended_event(self, sut) -> None:
        raw = '{"name": "turn_ended", "data": {}}'
        expected = TurnEndedEvent()

        result = sut.create(raw)

        assert result == expected

    def test_when_event_turn_started__returns_turn_started_event(self, sut) -> None:
        raw = '{"name": "turn_started", "data": {}}'
        expected = TurnStartedEvent()

        result = sut.create(raw)

        assert result == expected

    def test_when_event_user_joined__returns_user_joined_event(self, sut) -> None:
        raw = '{"name": "user_joined", "data": {"user": {"name": "Alice", "id": "123"}}}'
        expected = UserJoinedEvent(user=User(id="123", name="Alice"))

        result = sut.create(raw)

        assert result == expected

    def test_when_event_user_left__returns_user_left_event(self, sut) -> None:
        raw = '{"name": "user_left", "data": {"user": {"name": "Alice", "id": "123"}}}'
        expected = UserLeftEvent(user=User(id="123", name="Alice"))

        result = sut.create(raw)

        assert result == expected

    def test_when_event_unknown__raises_not_implemented_error(self, sut) -> None:
        raw = '{"name": "foo", "data": {}}'

        with pytest.raises(NotImplementedError):
            sut.create(raw)
