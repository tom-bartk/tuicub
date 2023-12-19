from typing import Any

from prompt_toolkit.layout import Container, Dimension, Window
from prompt_toolkit.renderer import WritePosition

from .base_container import BaseContainer, Renderer


class HCenterView(BaseContainer):
    """A view that renders horizontally centered content."""

    def __init__(
        self, content: Container, content_width: int, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self._left_window = Window(char=" ", always_hide_cursor=True)
        self._right_window = Window(char=" ", always_hide_cursor=True)
        self.content: Container = content
        self.content_width: int = content_width

    def preferred_height(self, width: int, max_available_height: int) -> Dimension:
        return self.content.preferred_height(width, max_available_height)

    def render(
        self, renderer: Renderer, write_position: WritePosition, parent_style: str
    ) -> None:  # pragma: no cover
        padding = (write_position.width - self.content_width) // 2
        if padding > 0:
            renderer.render(
                container=self._left_window,
                write_position=WritePosition(
                    xpos=write_position.xpos,
                    ypos=write_position.ypos,
                    width=padding,
                    height=write_position.height,
                ),
            )
            renderer.render(
                container=self._right_window,
                write_position=WritePosition(
                    xpos=write_position.xpos + self.content_width + padding,
                    ypos=write_position.ypos,
                    width=padding,
                    height=write_position.height,
                ),
            )

        renderer.render(
            container=self.content,
            write_position=WritePosition(
                xpos=write_position.xpos + padding,
                ypos=write_position.ypos,
                width=self.content_width,
                height=write_position.height,
            ),
        )

    def reset(self) -> None:
        self.content.reset()

    def get_children(self) -> list[Container]:
        return [self.content]


class VCenterView(BaseContainer):
    """A view that renders vertically centered content."""

    def __init__(
        self, content: Container, content_height: int, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self._top_window = Window(char=" ", always_hide_cursor=True)
        self._bottom_window = Window(char=" ", always_hide_cursor=True)
        self.content: Container = content
        self.content_height: int = content_height

    def preferred_width(self, max_available_width: int) -> Dimension:
        return self.content.preferred_width(max_available_width)

    def render(
        self, renderer: Renderer, write_position: WritePosition, parent_style: str
    ) -> None:  # pragma: no cover
        padding = (write_position.height - self.content_height) // 2
        if padding > 0:
            renderer.render(
                container=self._top_window,
                write_position=WritePosition(
                    xpos=write_position.xpos,
                    ypos=write_position.ypos,
                    width=write_position.width,
                    height=padding,
                ),
            )
            bottom_height = (
                padding + 1
                if (write_position.height - self.content_height) % 2 == 1
                else padding
            )
            renderer.render(
                container=self._bottom_window,
                write_position=WritePosition(
                    xpos=write_position.xpos,
                    ypos=write_position.ypos + self.content_height + padding,
                    width=write_position.width,
                    height=bottom_height,
                ),
            )

        renderer.render(
            container=self.content,
            write_position=WritePosition(
                xpos=write_position.xpos,
                ypos=write_position.ypos + padding,
                width=write_position.width,
                height=self.content_height,
            ),
        )

    def reset(self) -> None:
        self.content.reset()

    def get_children(self) -> list[Container]:
        return [self.content]
