import asyncio
from unittest.mock import Mock, create_autospec, patch

import pytest

from src.tuicub.common.views.animation import TextAnimation, TextAnimator


@pytest.fixture()
def sut() -> TextAnimator:
    return TextAnimator()


@pytest.fixture()
def animation() -> TextAnimation:
    animation = Mock()
    animation.animate = Mock()
    return animation


class TestAnimate:
    def test_creates_animation_task(self, sut, animation) -> None:
        with patch("asyncio.create_task") as mocked_create_task:
            sut.animate(animation=animation, side_effect=Mock())

            mocked_create_task.assert_called_once()

    def test_animates_with_side_effect(self, sut, animation) -> None:
        side_effect = Mock()

        with patch("asyncio.create_task"):
            sut.animate(animation=animation, side_effect=side_effect)

            animation.animate.assert_called_once_with(side_effect)

    def test_when_other_animation_running__cancels_previous_animation_task(
        self, sut, animation
    ) -> None:
        task_1 = create_autospec(asyncio.Task)
        task_1.cancelling = Mock(return_value=False)
        task_1.cancelled = Mock(return_value=False)

        task_2 = create_autospec(asyncio.Task)

        side_effect = Mock()

        with patch("asyncio.create_task", side_effect=[task_1, task_2]):
            sut.animate(animation=animation, side_effect=side_effect)
            sut.animate(animation=animation, side_effect=side_effect)

            task_1.cancel.assert_called_once()
