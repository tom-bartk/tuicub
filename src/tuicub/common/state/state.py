from attrs import field, frozen

from ..models import Game, Gameroom, User


@frozen
class State:
    """The global state of the application.

    Attributes:
        current_game (Game | None): An optional currently played game.
        current_gameroom (Gameroom | None): An optional gameroom that
            the current user created or joined.
        current_user (User | None): An optional current user.
        gamerooms (tuple[Gameroom, ...] | None): An optional list of
            currently stored active gamerooms.
    """

    current_game: Game | None = field(default=None)
    current_gameroom: Gameroom | None = field(default=None)
    current_user: User | None = field(default=None)
    gamerooms: tuple[Gameroom, ...] | None = field(default=None)
