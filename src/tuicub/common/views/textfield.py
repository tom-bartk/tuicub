from abc import abstractmethod
from typing import Protocol
from weakref import ReferenceType, ref

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindingsBase
from prompt_toolkit.layout import Container, Dimension, Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import FocusableElement
from prompt_toolkit.renderer import WritePosition
from prompt_toolkit.utils import to_str

from .base_container import BaseContainer, Renderer
from .color import Color, Theme

TEXTFIELD_HEIGHT = 3


class TextfieldViewDelegate(Protocol):
    """Delegate notified whenever the text of a textfield changes."""

    @abstractmethod
    def on_text_changed(self, text: str) -> None:
        """Called whenever the text of a textfield changes.

        Args:
            text (str): The new text.
        """


class TextfieldView(BaseContainer):
    """A view that serves as text input."""

    def __init__(
        self,
        text_color: Color | None = None,
        background_color: Color | None = None,
        theme: Theme | None = None,
    ) -> None:
        self._delegate: ReferenceType[TextfieldViewDelegate] | None = None
        self._theme: Theme = theme or Theme.default()

        self.buffer = Buffer(
            document=Document("", 0),
            multiline=False,
            on_text_changed=self._text_did_change,
        )
        self.buffer_control = BufferControl(
            buffer=Buffer(
                document=Document("", 0),
                multiline=False,
                on_text_changed=self._text_did_change,
            ),
            focusable=True,
        )

        self.input_container = Window(
            content=self.buffer_control,
            height=1,
            dont_extend_height=True,
            wrap_lines=False,
        )

        self._style = self._theme.to_framework_bg(background_color or Color.BG6)
        self._text_style = self._theme.to_framework_fg(text_color or Color.FG0)

        self._top_window = Window(char="▄", height=1)
        self._bottom_window = Window(char="▀", height=1)
        self._left_window = Window(char=" ", always_hide_cursor=True, style=self._style)
        self._right_window = Window(char=" ", always_hide_cursor=True, style=self._style)
        self.key_bindings: KeyBindingsBase | None = None

    def preferred_height(self, width: int, max_available_height: int) -> Dimension:
        return Dimension.exact(TEXTFIELD_HEIGHT)

    def render(
        self, renderer: Renderer, write_position: WritePosition, parent_style: str
    ) -> None:  # pragma: no cover
        style = f"{parent_style} {to_str(self._style)} {to_str(self._text_style)}"
        inverted_style = f"{parent_style} {to_str(self._style).replace('bg', 'fg')}"

        # Write "▀" and "▄" chars at the top and bottom for the whole width as a padding
        renderer.render(
            container=self._top_window,
            write_position=WritePosition(
                xpos=write_position.xpos,
                ypos=write_position.ypos,
                width=write_position.width,
                height=1,
            ),
            style=inverted_style,
        )
        renderer.render(
            container=self._bottom_window,
            write_position=WritePosition(
                xpos=write_position.xpos,
                ypos=write_position.ypos + 2,
                width=write_position.width,
                height=1,
            ),
            style=inverted_style,
        )

        # Write a single space characters to the left and right of the input as padding
        renderer.render(
            container=self._left_window,
            write_position=WritePosition(
                xpos=write_position.xpos,
                ypos=write_position.ypos + 1,
                width=1,
                height=1,
            ),
            style=inverted_style,
        )
        renderer.render(
            container=self._right_window,
            write_position=WritePosition(
                xpos=write_position.xpos + write_position.width - 1,
                ypos=write_position.ypos + 1,
                width=1,
                height=1,
            ),
            style=inverted_style,
        )

        # Write the input itself
        renderer.render(
            container=self.input_container,
            write_position=WritePosition(
                xpos=write_position.xpos + 1,
                ypos=write_position.ypos + 1,
                width=write_position.width - 2,
                height=1,
            ),
            style=style,
        )

    def reset(self) -> None:
        self.buffer_control.reset()

    def set_delegate(self, delegate: TextfieldViewDelegate) -> None:
        self._delegate = ref(delegate)

    def _text_did_change(self, buffer: Buffer) -> None:
        if self._delegate and (delegate := self._delegate()):
            delegate.on_text_changed(buffer.text)

    def get_children(self) -> list[Container]:
        return [self.input_container]

    def focus_target(self) -> FocusableElement:
        return self.buffer_control
