import asyncio
from collections.abc import Generator
from weakref import WeakMethod

from attrs import field, frozen
from prompt_toolkit import application

from .text import Text


@frozen
class TextAnimation:
    """An animation of a changing text.

    Attributes:
        frames: (Generator[Text, None, None]): The generator producing
            text frames to animate.
        fps (int): The framerate to use when rendering the animation.
    """

    frames: Generator[Text, None, None] = field(eq=False)
    fps: int

    async def animate(self, side_effect: WeakMethod) -> None:
        """Perform the animation.

        The side effect is called before each frame produced by the generator.

        Args:
            side_effect (WeakMethod): The side effect called before each frame.
        """
        for text in self.frames:
            if _side_effect := side_effect():
                _side_effect(text)

            application.get_app().invalidate()

            if self.fps > 0:
                await asyncio.sleep(1 / self.fps)


class TextAnimator:
    """An animator that executes text animations."""

    __slots__ = ("_animation_task",)

    def __init__(self) -> None:
        self._animation_task: asyncio.Task | None = None

    def animate(self, animation: TextAnimation, side_effect: WeakMethod) -> None:
        """Animate a text animation with side effect called before each frame.

        Args:
            animation (TextAnimation): The animation to run.
            side_effect (WeakMethod): The side effect called before each frame.
        """
        if self._animation_task and (
            not self._animation_task.cancelled() or not self._animation_task.cancelling()
        ):
            self._animation_task.cancel()

        self._animation_task = asyncio.create_task(animation.animate(side_effect))
