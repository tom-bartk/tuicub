from collections.abc import Generator
from unittest.mock import Mock, call, create_autospec, patch

import pytest

from src.tuicub.common.models import Alert, AlertType, Gameroom, remove_gameroom
from src.tuicub.common.views import Color, Text, TextPart
from src.tuicub.common.views.animation import TextAnimation
from src.tuicub.common.views.text import EMPTY_TEXT


class TestRemoveGameroom:
    def test_when_gameroom_with_id_is_present__returns_tuple_without_gameroom(
        self,
    ) -> None:
        gameroom_1 = create_autospec(Gameroom)
        gameroom_1.id = "1"
        gameroom_2 = create_autospec(Gameroom)
        gameroom_2.id = "2"
        gameroom_3 = create_autospec(Gameroom)
        gameroom_3.id = "3"

        expected = (gameroom_1, gameroom_3)

        result = remove_gameroom(
            gameroom_id="2", gamerooms=(gameroom_1, gameroom_2, gameroom_3)
        )

        assert result == expected

    def test_when_gameroom_with_id_is_not_present__returns_unchanged_tuple(
        self,
    ) -> None:
        gameroom_1 = create_autospec(Gameroom)
        gameroom_1.id = "1"
        gameroom_2 = create_autospec(Gameroom)
        gameroom_2.id = "2"
        gameroom_3 = create_autospec(Gameroom)
        gameroom_3.id = "3"

        expected = (gameroom_1, gameroom_2, gameroom_3)

        result = remove_gameroom(
            gameroom_id="4", gamerooms=(gameroom_1, gameroom_2, gameroom_3)
        )

        assert result == expected


class TestAlertType:
    @pytest.mark.parametrize(
        ("sut", "expected"),
        [
            (AlertType.ERROR, Color.RED),
            (AlertType.INFO, Color.BLUE),
            (AlertType.SUCCESS, Color.GREEN_LIGHT),
            (AlertType.WARNING, Color.ORANGE),
        ],
    )
    def test_color__returns_correct_color_for_type(self, sut, expected) -> None:
        result = sut.color

        assert result == expected

    def test_animation_duration__when_info__returns_5(self) -> None:
        sut = AlertType.INFO
        expected = 5

        result = sut.animation_duration

        assert result == expected

    def test_animation_duration__when_not_info__returns_3(self) -> None:
        sut = AlertType.SUCCESS
        expected = 3

        result = sut.animation_duration

        assert result == expected

    def test_animation_fps__when_info__returns_2(self) -> None:
        sut = AlertType.INFO
        expected = 2

        result = sut.animation_fps

        assert result == expected

    def test_animation_fps__when_not_info__returns_4(self) -> None:
        sut = AlertType.SUCCESS
        expected = 4

        result = sut.animation_fps

        assert result == expected


class TestAlert:
    @pytest.mark.parametrize(
        ("sut", "expected"),
        [
            (Alert("foo", AlertType.ERROR), TextPart(" ⚠  foo ", fg=Color.RED)),
            (Alert("foo", AlertType.WARNING), TextPart(" ⚠  foo ", fg=Color.ORANGE)),
            (Alert("foo", AlertType.INFO), TextPart(" ℹ foo ", fg=Color.BLUE)),
            (Alert("foo", AlertType.SUCCESS), TextPart(" ✔ foo ", fg=Color.GREEN_LIGHT)),
        ],
    )
    def test_text_parts__returns_correct_text_and_color(self, sut, expected) -> None:
        result = sut.text_part

        assert result == expected

    def test_animation_frames__returns_correct_generator_of_texts(self) -> None:
        sut = Alert("foo", AlertType.ERROR)
        expected = (
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━━━━━━━━━━", Color.RED),
                TextPart("", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━━━━━━━━━", Color.RED),
                TextPart("━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━━━━━━━━", Color.RED),
                TextPart("━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━━━━━━━", Color.RED),
                TextPart("━━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━━━━━━", Color.RED),
                TextPart("━━━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━━━━━", Color.RED),
                TextPart("━━━━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━━━━", Color.RED),
                TextPart("━━━━━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━━━", Color.RED),
                TextPart("━━━━━━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━━", Color.RED),
                TextPart("━━━━━━━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━━", Color.RED),
                TextPart("━━━━━━━━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━━", Color.RED),
                TextPart("━━━━━━━━━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("━", Color.RED),
                TextPart("━━━━━━━━━━━", Color.BG8),
            ),
            Text(
                TextPart(" ⚠  foo ", fg=Color.RED),
                TextPart("", Color.RED),
                TextPart("━━━━━━━━━━━━", Color.BG8),
            ),
            EMPTY_TEXT,
        )

        result = tuple(sut.animation_frames)

        assert result == expected

    def test_animation__returns_text_animation(self) -> None:
        sut = Alert("foo", AlertType.ERROR)
        expected = TextAnimation(frames=sut.animation_frames, fps=4)

        result = sut.animation

        assert result == expected


class TestTextAnimation:
    @pytest.mark.asyncio()
    async def test_animate__sleeps_for_each_frame_for_one_div_by_fps_seconds(
        self, get_app, app
    ) -> None:
        text_1 = Mock()
        text_2 = Mock()
        text_3 = Mock()

        def frames() -> Generator[Text, None, None]:
            yield text_1
            yield text_2
            yield text_3

        sut = TextAnimation(frames=frames(), fps=10)

        expected_calls = [
            call(1 / 10),
            call(1 / 10),
            call(1 / 10),
        ]

        with patch("prompt_toolkit.application.get_app", new=get_app), patch(
            "asyncio.sleep"
        ) as mocked_sleep:
            await sut.animate(side_effect=Mock(return_value=Mock()))

            mocked_sleep.assert_has_calls(expected_calls)

    @pytest.mark.asyncio()
    async def test_animate__calls_side_effect_with_each_text_frame(
        self, get_app, app
    ) -> None:
        text_1 = Mock()
        text_2 = Mock()
        text_3 = Mock()

        def frames() -> Generator[Text, None, None]:
            yield text_1
            yield text_2
            yield text_3

        side_effect = Mock()
        weak_side_effect = Mock(return_value=side_effect)
        sut = TextAnimation(frames=frames(), fps=10)

        expected_calls = [
            call(text_1),
            call(text_2),
            call(text_3),
        ]

        with patch("prompt_toolkit.application.get_app", new=get_app), patch(
            "asyncio.sleep"
        ):
            await sut.animate(side_effect=weak_side_effect)

            side_effect.assert_has_calls(expected_calls)

    @pytest.mark.asyncio()
    async def test_animate__invalidates_app_for_each_frame(self, get_app, app) -> None:
        text_1 = Mock()
        text_2 = Mock()
        text_3 = Mock()

        def frames() -> Generator[Text, None, None]:
            yield text_1
            yield text_2
            yield text_3

        side_effect = Mock()
        weak_side_effect = Mock(return_value=side_effect)
        sut = TextAnimation(frames=frames(), fps=10)

        with patch("prompt_toolkit.application.get_app", new=get_app), patch(
            "asyncio.sleep"
        ):
            await sut.animate(side_effect=weak_side_effect)

            assert app.invalidate.call_count == 3
