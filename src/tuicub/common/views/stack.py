from __future__ import annotations

from collections.abc import Callable, Sequence

from attrs import frozen
from prompt_toolkit.key_binding import KeyBindingsBase
from prompt_toolkit.layout import (
    AnyDimension,
    Container,
    Dimension,
    FormattedTextControl,
    HSplit,
    VerticalAlign,
    Window,
)
from prompt_toolkit.layout.mouse_handlers import MouseHandlers
from prompt_toolkit.renderer import Screen, WritePosition
from prompt_toolkit.utils import to_str

from .color import AnyBackgroundColor, Theme, to_framework_bg


def _window_too_small() -> Window:
    return Window(
        FormattedTextControl(text=[("class:window-too-small", " Window too small... ")])
    )


@frozen
class Padding:
    left: int
    right: int
    top: int
    bottom: int

    @classmethod
    def zero(cls) -> Padding:
        return Padding(0, 0, 0, 0)

    @classmethod
    def horizontal(cls, value: int) -> Padding:
        return Padding(left=value, right=value, top=0, bottom=0)


class StackView(HSplit):
    """A view that draws its children stacked horizontally."""

    @property
    def _all_children(
        self,
    ) -> list[Container]:  # pragma: no cover # overriding private property of HSplit
        match self.align:
            case VerticalAlign.TOP:
                if self.dont_extend_height:
                    return list(self._children())
                return [*self._children(), self._fill_bottom]
            case VerticalAlign.CENTER:
                return [
                    self._fill_top,
                    *self._children(),
                    self._fill_bottom,
                ]
            case VerticalAlign.BOTTOM:
                return [self._fill_top, *self._children()]
            case VerticalAlign.JUSTIFY:
                return list(self._children())

    @property
    def children(self) -> list[Container]:  # type: ignore
        return list(self._children())

    def __init__(
        self,
        children: Callable[[], Sequence[Container]],
        background_color: AnyBackgroundColor | None = None,
        align: VerticalAlign = VerticalAlign.TOP,
        width: AnyDimension | None = None,
        height: AnyDimension | None = None,
        key_bindings: KeyBindingsBase | None = None,
        padding: Padding | None = None,
        theme: Theme | None = None,
        dont_extend_height: bool = False,
    ) -> None:
        self._children: Callable[[], Sequence[Container]] = children
        self.window_too_small = _window_too_small()
        self.width = width
        self.height = height
        self.align = align
        self.z_index = 0
        self.modal = False
        self.key_bindings = key_bindings
        self.dont_extend_height: bool = dont_extend_height
        self.style = to_framework_bg(background_color, theme or Theme.default())
        self._remaining_space_window = Window(style=self.style)
        self._fill_top = Window(width=Dimension(preferred=0), style=self.style)
        self._fill_bottom = Window(width=Dimension(preferred=0), style=self.style)
        self._padding: Padding = padding or Padding.zero()

        self._padding_left: Window | None = (
            Window(
                width=Dimension(preferred=self._padding.left),
                dont_extend_width=True,
                style=self.style,
            )
            if self._padding.left
            else None
        )
        self._padding_right: Window | None = (
            Window(
                width=Dimension(preferred=self._padding.right),
                dont_extend_width=True,
                style=self.style,
            )
            if self._padding.right
            else None
        )
        self._padding_top: Window | None = (
            Window(
                height=Dimension(preferred=self._padding.top),
                dont_extend_height=True,
                style=self.style,
            )
            if self._padding.top
            else None
        )
        self._padding_bottom: Window | None = (
            Window(
                height=Dimension(preferred=self._padding.bottom),
                dont_extend_height=True,
                style=self.style,
            )
            if self._padding.bottom
            else None
        )

    @classmethod
    def with_subviews(
        cls,
        *subviews: Container,
        background_color: AnyBackgroundColor | None = None,
        align: VerticalAlign = VerticalAlign.TOP,
        width: AnyDimension | None = None,
        height: AnyDimension | None = None,
        key_bindings: KeyBindingsBase | None = None,
        padding: Padding | None = None,
        theme: Theme | None = None,
        dont_extend_height: bool = False,
    ) -> StackView:
        return StackView(
            children=lambda: subviews,
            background_color=background_color,
            align=align,
            width=width,
            height=height,
            key_bindings=key_bindings,
            padding=padding,
            theme=theme,
            dont_extend_height=dont_extend_height,
        )

    def write_to_screen(
        self,
        screen: Screen,
        mouse_handlers: MouseHandlers,
        write_position: WritePosition,
        parent_style: str,
        erase_bg: bool,
        z_index: int | None,
    ) -> None:  # pragma: no cover
        style = f"{parent_style} {to_str(self.style)}"
        left_width = 0
        if left := self._padding_left:
            left_width = left.preferred_width(
                max_available_width=write_position.width
            ).preferred
            left.write_to_screen(
                screen,
                mouse_handlers,
                WritePosition(
                    write_position.xpos,
                    write_position.ypos,
                    left_width,
                    write_position.height,
                ),
                style,
                erase_bg,
                z_index,
            )

        right_width = 0
        if right := self._padding_right:
            right_width = right.preferred_width(
                max_available_width=write_position.width
            ).preferred
            right.write_to_screen(
                screen,
                mouse_handlers,
                WritePosition(
                    write_position.xpos + write_position.width - right_width,
                    write_position.ypos,
                    right_width,
                    write_position.height,
                ),
                style,
                erase_bg,
                z_index,
            )

        width_minus_padding = write_position.width - left_width - right_width

        top_height = 0
        if top := self._padding_top:
            top_height = top.preferred_height(
                width=width_minus_padding, max_available_height=write_position.height
            ).preferred
            top.write_to_screen(
                screen,
                mouse_handlers,
                write_position,
                style,
                erase_bg,
                z_index,
            )

        bottom_height = 0
        if bottom := self._padding_bottom:
            bottom_height = bottom.preferred_height(
                width=width_minus_padding, max_available_height=write_position.height
            ).preferred
            bottom.write_to_screen(
                screen,
                mouse_handlers,
                WritePosition(
                    write_position.xpos,
                    write_position.ypos + write_position.height - bottom_height,
                    write_position.width,
                    write_position.height,
                ),
                style,
                erase_bg,
                z_index,
            )

        height_minus_padding = write_position.height - top_height - bottom_height

        super().write_to_screen(
            screen,
            mouse_handlers,
            WritePosition(
                write_position.xpos + left_width,
                write_position.ypos + top_height,
                width_minus_padding,
                height_minus_padding,
            ),
            parent_style,
            erase_bg,
            z_index,
        )
