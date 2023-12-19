from unittest.mock import Mock, create_autospec, patch

import pendulum

from src.tuicub.common.models import Gameroom, GameroomStatus
from src.tuicub.common.strings import GAMEROOM_CREATED_AT_PREFIX, GAMEROOM_JUST_CREATED
from src.tuicub.common.views.color import Color
from src.tuicub.common.views.gameroom import (
    badge,
    created_at_diff,
    gameroom_text,
    separator,
    squares_color,
)
from src.tuicub.common.views.text import Text, TextPart

MAX_PLAYERS_COUNT = 4


class TestSquaresColor:
    def test_when_gameroom_has_1_user__returns_green_dark(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.users = (Mock(),)
        expected = Color.GREEN_DARK

        result = squares_color(gameroom=gameroom)

        assert result == expected

    def test_when_gameroom_has_2_users__returns_yellow_dark(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.users = (Mock(), Mock())
        expected = Color.YELLOW_DARK

        result = squares_color(gameroom=gameroom)

        assert result == expected

    def test_when_gameroom_has_3_users__returns_orange_dark(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.users = (Mock(), Mock(), Mock())
        expected = Color.ORANGE_DARK

        result = squares_color(gameroom=gameroom)

        assert result == expected

    def test_when_gameroom_has_4_users__returns_red_dark(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.users = (Mock(), Mock(), Mock(), Mock())
        expected = Color.RED_DARK

        result = squares_color(gameroom=gameroom)

        assert result == expected


class TestCreatedAtDiff:
    def test_when_created_at_more_than_1_minute_ago__returns_diff_for_humans(
        self, gameroom
    ) -> None:
        created_at = Mock()
        diff = create_autospec(pendulum.Interval)
        diff.in_minutes = Mock(return_value=42)
        created_at.diff = Mock(return_value=diff)
        expected = "foo"
        created_at.diff_for_humans = Mock(return_value=expected)

        with patch("pendulum.instance", return_value=created_at):
            result = created_at_diff(gameroom=gameroom)

            assert result == expected

    def test_when_created_at_less_than_1_minute_ago__returns_gameroom_just_created(
        self, gameroom
    ) -> None:
        created_at = Mock()
        diff = create_autospec(pendulum.Interval)
        diff.in_minutes = Mock(return_value=0)
        created_at.diff = Mock(return_value=diff)
        expected = GAMEROOM_JUST_CREATED
        created_at.diff_for_humans = Mock(return_value=expected)

        with patch("pendulum.instance", return_value=created_at):
            result = created_at_diff(gameroom=gameroom)

            assert result == expected


class TestSeparator:
    def test_when_gameroom_starting__prefix_justified_left_to_5(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.status = GameroomStatus.STARTING
        expected = TextPart("  Ⅰ  ", fg=Color.FG1)

        result = separator(gameroom, fg=Color.FG1)

        assert result == expected

    def test_when_gameroom_finished__prefix_justified_left_to_5(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.status = GameroomStatus.FINISHED
        expected = TextPart("  Ⅰ  ", fg=Color.FG1)

        result = separator(gameroom, fg=Color.FG1)

        assert result == expected

    def test_when_gameroom_running__prefix_justified_left_to_6(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.status = GameroomStatus.RUNNING
        expected = TextPart("  Ⅰ   ", fg=Color.FG1)

        result = separator(gameroom, fg=Color.FG1)

        assert result == expected

    def test_when_gameroom_deleted__prefix_justified_left_to_6(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.status = GameroomStatus.DELETED
        expected = TextPart("  Ⅰ   ", fg=Color.FG1)

        result = separator(gameroom, fg=Color.FG1)

        assert result == expected


class TestBadge:
    def test_when_gameroom_starting__fg_green_light__bg_green_dim(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.status = GameroomStatus.STARTING
        expected = TextPart(
            " STARTING ", fg=Color.GREEN_LIGHT, bg=Color.GREEN_DIM, bold=True
        )

        result = badge(gameroom)

        assert result == expected

    def test_when_gameroom_running__fg_yellow_light__bg_yellow_dim(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.status = GameroomStatus.RUNNING
        expected = TextPart(
            " RUNNING ", fg=Color.YELLOW_LIGHT, bg=Color.YELLOW_DIM, bold=True
        )

        result = badge(gameroom)

        assert result == expected

    def test_when_gameroom_finished__fg_red__bg_red_dim(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.status = GameroomStatus.FINISHED
        expected = TextPart(" FINISHED ", fg=Color.RED, bg=Color.RED_DIM, bold=True)

        result = badge(gameroom)

        assert result == expected


class TestGameroomText:
    def test_when_highlighted__gray_shade_is_bg8(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.status = GameroomStatus.STARTING
        gameroom.users = (Mock(),)
        gameroom.name = "foo"

        created_at = Mock()
        diff = create_autospec(pendulum.Interval)
        diff.in_minutes = Mock(return_value=42)
        created_at.diff = Mock(return_value=diff)
        created_at.diff_for_humans = Mock(return_value="bar")

        expected = Text(
            TextPart("\n  foo ", Color.FG0),
            TextPart.flex(),
            TextPart("■", Color.GREEN_DARK),
            TextPart("□□□", Color.BG8),
            TextPart(" 1/4", Color.FG3),
            TextPart("  Ⅰ  ", fg=Color.BG8),
            TextPart(" STARTING ", fg=Color.GREEN_LIGHT, bg=Color.GREEN_DIM, bold=True),
            TextPart(f"  \n  {GAMEROOM_CREATED_AT_PREFIX} bar.", Color.FG4),
        )

        with patch("pendulum.instance", return_value=created_at):
            result = gameroom_text(gameroom=gameroom, is_highlighted=True)
            assert result == expected

    def test_when_not_highlighted__gray_shade_is_bg6(self) -> None:
        gameroom = create_autospec(Gameroom)
        gameroom.status = GameroomStatus.RUNNING
        gameroom.users = (Mock(), Mock())
        gameroom.name = "foo"

        created_at = Mock()
        diff = create_autospec(pendulum.Interval)
        diff.in_minutes = Mock(return_value=42)
        created_at.diff = Mock(return_value=diff)
        created_at.diff_for_humans = Mock(return_value="bar")

        expected = Text(
            TextPart("\n  foo ", Color.FG0),
            TextPart.flex(),
            TextPart("■■", Color.YELLOW_DARK),
            TextPart("□□", Color.BG6),
            TextPart(" 2/4", Color.FG3),
            TextPart("  Ⅰ   ", fg=Color.BG6),
            TextPart(" RUNNING ", fg=Color.YELLOW_LIGHT, bg=Color.YELLOW_DIM, bold=True),
            TextPart(f"  \n  {GAMEROOM_CREATED_AT_PREFIX} bar.", Color.FG4),
        )

        with patch("pendulum.instance", return_value=created_at):
            result = gameroom_text(gameroom=gameroom, is_highlighted=False)
            assert result == expected
