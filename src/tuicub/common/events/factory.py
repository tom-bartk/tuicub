from attrs import frozen
from eventoolkit import Event, EventsFactory
from marshmallow_generic import EXCLUDE

from ...game.events import (
    BoardChangedEventSchema,
    PileCountChangedEventSchema,
    PlayerLeftEventSchema,
    PlayersChangedEventSchema,
    PlayerWonEventSchema,
    RackChangedEventSchema,
    TileDrawnEventSchema,
    TurnEndedEvent,
    TurnStartedEvent,
)
from ...gameroom.events import (
    GameroomDeletedEventSchema,
    GameStartedEventSchema,
    UserJoinedEventSchema,
    UserLeftEventSchema,
)
from ..schemas import TuicubEventSchema
from .event import EventName, TuicubEvent


@frozen
class EventSchemas:
    base_schema: TuicubEventSchema
    board_changed: BoardChangedEventSchema
    game_started: GameStartedEventSchema
    gameroom_deleted: GameroomDeletedEventSchema
    pile_count_changed: PileCountChangedEventSchema
    player_left: PlayerLeftEventSchema
    player_won: PlayerWonEventSchema
    players_changed: PlayersChangedEventSchema
    rack_changed: RackChangedEventSchema
    tile_drawn: TileDrawnEventSchema
    user_joined: UserJoinedEventSchema
    user_left: UserLeftEventSchema


class TuicubEventsFactory(EventsFactory):
    """A factory creating events based on the event name."""

    __slots__ = ("_schemas",)

    def __init__(self, event_schemas: EventSchemas):
        """Initialize new factory.

        Args:
            event_schemas (EventSchemas): Schemas for all application events.
        """
        self._schemas: EventSchemas = event_schemas

    def create(self, raw: str) -> Event:  # noqa: PLR0911
        """Create a new event from the raw string.

        First, the input is deserialized into a `TuicubEvent`. Then, the event's
        data is deserialized into an application event based on the event's name.

        Args:
            raw (str): The raw representation of the event.

        Returns:
            The created application event.
        """
        event: TuicubEvent = self._schemas.base_schema.loads(raw, unknown=EXCLUDE)

        match event.name:
            case EventName.BOARD_CHANGED:
                return self._schemas.board_changed.load(event.data, unknown=EXCLUDE)
            case EventName.GAME_STARTED:
                return self._schemas.game_started.load(event.data, unknown=EXCLUDE)
            case EventName.GAMEROOM_DELETED:
                return self._schemas.gameroom_deleted.load(event.data, unknown=EXCLUDE)
            case EventName.PILE_COUNT_CHANGED:
                return self._schemas.pile_count_changed.load(event.data, unknown=EXCLUDE)
            case EventName.PLAYER_LEFT:
                return self._schemas.player_left.load(event.data, unknown=EXCLUDE)
            case EventName.PLAYER_WON:
                return self._schemas.player_won.load(event.data, unknown=EXCLUDE)
            case EventName.PLAYERS_CHANGED:
                return self._schemas.players_changed.load(event.data, unknown=EXCLUDE)
            case EventName.RACK_CHANGED:
                return self._schemas.rack_changed.load(event.data, unknown=EXCLUDE)
            case EventName.TILE_DRAWN:
                return self._schemas.tile_drawn.load(event.data, unknown=EXCLUDE)
            case EventName.TURN_ENDED:
                return TurnEndedEvent()
            case EventName.TURN_STARTED:
                return TurnStartedEvent()
            case EventName.USER_JOINED:
                return self._schemas.user_joined.load(event.data, unknown=EXCLUDE)
            case EventName.USER_LEFT:
                return self._schemas.user_left.load(event.data, unknown=EXCLUDE)
            case _:
                raise NotImplementedError
