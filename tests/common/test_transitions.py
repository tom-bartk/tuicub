from pyllot import TransitionDirection

from src.tuicub.common.screens import ScreenName
from src.tuicub.common.state import State
from src.tuicub.common.transitions import (
    GAME_TO_GAMEROOMS,
    GAMEROOM_TO_GAME,
    GAMEROOM_TO_GAMEROOMS,
    GAMEROOMS_TO_GAMEROOM,
    REGISTER_USER_TO_GAMEROOMS,
    HasCurrentGame,
    HasCurrentGameroom,
    HasCurrentUser,
    HasNoCurrentGame,
    HasNoCurrentGameroom,
)


class TestRegisterUserToGamerooms:
    def test_push__source_register_user__destination_gamerooms(self) -> None:
        assert REGISTER_USER_TO_GAMEROOMS.source == ScreenName.REGISTER_USER
        assert REGISTER_USER_TO_GAMEROOMS.destination == ScreenName.GAMEROOMS
        assert REGISTER_USER_TO_GAMEROOMS.direction == TransitionDirection.PUSH

    def test_condition_is_has_current_user(self) -> None:
        assert isinstance(
            REGISTER_USER_TO_GAMEROOMS._condition, HasCurrentUser  # noqa: SLF001
        )


class TestGameroomsToGameroom:
    def test_push__source_gamerooms__destination_gameroom(self) -> None:
        assert GAMEROOMS_TO_GAMEROOM.source == ScreenName.GAMEROOMS
        assert GAMEROOMS_TO_GAMEROOM.destination == ScreenName.GAMEROOM
        assert GAMEROOMS_TO_GAMEROOM.direction == TransitionDirection.PUSH

    def test_condition_is_has_current_gameroom(self) -> None:
        assert isinstance(
            GAMEROOMS_TO_GAMEROOM._condition, HasCurrentGameroom  # noqa: SLF001
        )


class TestGameroomToGame:
    def test_push__source_gameroom__destination_game(self) -> None:
        assert GAMEROOM_TO_GAME.source == ScreenName.GAMEROOM
        assert GAMEROOM_TO_GAME.destination == ScreenName.GAME
        assert GAMEROOM_TO_GAME.direction == TransitionDirection.PUSH

    def test_condition_is_has_current_game(self) -> None:
        assert isinstance(GAMEROOM_TO_GAME._condition, HasCurrentGame)  # noqa: SLF001


class TestGameToGamerooms:
    def test_pop__source_game__destination_gamerooms(self) -> None:
        assert GAME_TO_GAMEROOMS.source == ScreenName.GAME
        assert GAME_TO_GAMEROOMS.destination == ScreenName.GAMEROOMS
        assert GAME_TO_GAMEROOMS.direction == TransitionDirection.POP

    def test_condition_is_has_no_current_game(self) -> None:
        assert isinstance(GAME_TO_GAMEROOMS._condition, HasNoCurrentGame)  # noqa: SLF001


class TestGameroomToGamerooms:
    def test_pop__source_gameroom__destination_gameroom(self) -> None:
        assert GAMEROOM_TO_GAMEROOMS.source == ScreenName.GAMEROOM
        assert GAMEROOM_TO_GAMEROOMS.destination == ScreenName.GAMEROOMS
        assert GAMEROOM_TO_GAMEROOMS.direction == TransitionDirection.POP

    def test_condition_is_has_no_current_gameroom(self) -> None:
        assert isinstance(
            GAMEROOM_TO_GAMEROOMS._condition, HasNoCurrentGameroom  # noqa: SLF001
        )


class TestHasCurrentUser:
    def test_when_has_current_user__returns_true(self, user) -> None:
        sut = HasCurrentUser()
        expected = True

        result = sut(state=State(current_user=user))

        assert result == expected

    def test_when_has_no_current_user__returns_false(self) -> None:
        sut = HasCurrentUser()
        expected = False

        result = sut(state=State(current_user=None))

        assert result == expected


class TestHasCurrentGameroom:
    def test_when_has_current_gameroom__returns_true(self, gameroom) -> None:
        sut = HasCurrentGameroom()
        expected = True

        result = sut(state=State(current_gameroom=gameroom))

        assert result == expected

    def test_when_has_no_current_gameroom__returns_false(self) -> None:
        sut = HasCurrentGameroom()
        expected = False

        result = sut(state=State(current_gameroom=None))

        assert result == expected


class TestHasCurrentGame:
    def test_when_has_current_game__returns_true(self, game) -> None:
        sut = HasCurrentGame()
        expected = True

        result = sut(state=State(current_game=game))

        assert result == expected

    def test_when_has_no_current_game__returns_false(self) -> None:
        sut = HasCurrentGame()
        expected = False

        result = sut(state=State(current_game=None))

        assert result == expected


class TestHasNoCurrentGameroom:
    def test_when_has_current_gameroom__returns_false(self, gameroom) -> None:
        sut = HasNoCurrentGameroom()
        expected = False

        result = sut(state=State(current_gameroom=gameroom))

        assert result == expected

    def test_when_has_no_current_gameroom__returns_true(self) -> None:
        sut = HasNoCurrentGameroom()
        expected = True

        result = sut(state=State(current_gameroom=None))

        assert result == expected


class TestHasNoCurrentGame:
    def test_when_has_current_game__returns_false(self, game) -> None:
        sut = HasNoCurrentGame()
        expected = False

        result = sut(state=State(current_game=game))

        assert result == expected

    def test_when_has_no_current_game__returns_true(self) -> None:
        sut = HasNoCurrentGame()
        expected = True

        result = sut(state=State(current_game=None))

        assert result == expected
