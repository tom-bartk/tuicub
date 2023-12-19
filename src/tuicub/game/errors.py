from ..common.strings import (
    GAME_NO_CURRENT_GAME_ERROR_MESSAGE,
    GAME_NO_CURRENT_USER_ERROR_MESSAGE,
)


class NoCurrentGameError(ValueError):
    def __init__(self):
        super().__init__(GAME_NO_CURRENT_GAME_ERROR_MESSAGE)


class NoCurrentUserError(ValueError):
    def __init__(self):
        super().__init__(GAME_NO_CURRENT_USER_ERROR_MESSAGE)
