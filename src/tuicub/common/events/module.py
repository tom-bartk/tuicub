import asyncio

import asockit
from eventoolkit import EventInputBridge, EventPublisher

from ...game.events import (
    BoardChangedEventSchema,
    PileCountChangedEventSchema,
    PlayerLeftEventSchema,
    PlayersChangedEventSchema,
    PlayerWonEventSchema,
    RackChangedEventSchema,
    TileDrawnEventSchema,
)
from ...gameroom.events import (
    GameroomDeletedEventSchema,
    GameStartedEventSchema,
    UserJoinedEventSchema,
    UserLeftEventSchema,
)
from ..schemas import TuicubEventSchema
from .factory import EventSchemas, TuicubEventsFactory


class EventsModule:
    __slots__ = ("_publisher", "_reader", "_writer", "_bridge")

    @property
    def publisher(self) -> EventPublisher:
        return self._publisher

    @property
    def socket_reader(self) -> asockit.SocketReader:
        return self._reader

    @property
    def socket_writer(self) -> asockit.SocketWriter:
        return self._writer

    def __init__(
        self, stream_reader: asyncio.StreamReader, stream_writer: asyncio.StreamWriter
    ):
        event_schemas = EventSchemas(
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
        self._publisher = EventPublisher()
        self._bridge = EventInputBridge(
            factory=TuicubEventsFactory(event_schemas=event_schemas),
            publisher=self._publisher,
        )

        self._reader = asockit.SocketReader(
            asockit.AsyncioReadableConnection(stream_reader)
        )
        self._writer = asockit.SocketWriter(
            asockit.AsyncioWritableConnection(stream_writer)
        )
        self._reader.set_delegate(self._bridge)
