from ..common.strings import GAMEROOM_NO_CURRENT_GAMEROOM_ERROR_MESSAGE


class NoCurrentGameroomError(ValueError):
    def __init__(self):
        super().__init__(GAMEROOM_NO_CURRENT_GAMEROOM_ERROR_MESSAGE)
