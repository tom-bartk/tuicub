from typing import Any

from marshmallow_generic import GenericSchema, fields

from .events.event import TuicubEvent
from .models import Game, Gameroom, GameroomStatus, GameState, Player, User


class TuicubEventSchema(GenericSchema[TuicubEvent]):
    name = fields.Str()
    data = fields.Dict()


class UserSchema(GenericSchema[User]):
    id = fields.Str()
    name = fields.Str()


class GameroomSchema(GenericSchema[Gameroom]):
    id = fields.Str()
    name = fields.Str()
    status = fields.Enum(GameroomStatus, by_value=True)
    created_at = fields.DateTime(format="timestamp_ms")
    owner_id = fields.Str()
    game_id = fields.Str(required=False, allow_none=True)
    users = fields.Method(deserialize="deserialize_users")

    def deserialize_users(self, obj: Any) -> tuple[User, ...]:
        users: list[User] = UserSchema().load(obj, many=True)
        return tuple(users)


class PlayerSchema(GenericSchema[Player]):
    name = fields.Str()
    user_id = fields.Str(required=False, allow_none=True)
    tiles_count = fields.Int()
    has_turn = fields.Bool()


class GameStateSchema(GenericSchema[GameState]):
    players = fields.List(fields.Nested(PlayerSchema))
    board = fields.List(fields.List(fields.Int))
    pile_count = fields.Int()
    rack = fields.List(fields.Int)


class GameSchema(GenericSchema[Game]):
    id = fields.Str()
    gameroom_id = fields.Str(required=False, allow_none=True)
    game_state = fields.Nested(GameStateSchema)
    winner = fields.Nested(PlayerSchema, required=False, allow_none=True)
