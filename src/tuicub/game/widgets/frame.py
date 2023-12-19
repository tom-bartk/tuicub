from __future__ import annotations

from attrs import frozen
from prompt_toolkit.layout.screen import WritePosition


@frozen
class Frame:
    """A frame of a widget."""

    x: int
    y: int
    width: int
    height: int

    @classmethod
    def from_write_position(cls, write_position: WritePosition) -> Frame:
        return Frame(
            write_position.xpos,
            write_position.ypos,
            write_position.width,
            write_position.height,
        )

    def to_write_position(self) -> WritePosition:
        return WritePosition(self.x, self.y, self.width, self.height)
