from enum import StrEnum

from attrs import frozen
from eventoolkit import Event


class EventName(StrEnum):
    GAME_STARTED = "game_started"
    GAMEROOM_DELETED = "gameroom_deleted"
    USER_JOINED = "user_joined"
    USER_LEFT = "user_left"

    BOARD_CHANGED = "board_changed"
    PILE_COUNT_CHANGED = "pile_count_changed"
    PLAYER_LEFT = "player_left"
    PLAYER_WON = "player_won"
    PLAYERS_CHANGED = "players_changed"
    RACK_CHANGED = "rack_changed"
    TILE_DRAWN = "tile_drawn"
    TURN_ENDED = "turn_ended"
    TURN_STARTED = "turn_started"


@frozen
class TuicubEvent(Event):
    """A structure for an event that wraps an application event.

    Attributes:
        name (str): The name of the event.
        data (dict): The event's payload containing an application event.
    """

    name: str
    data: dict
