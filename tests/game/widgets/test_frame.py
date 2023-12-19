from prompt_toolkit.layout.screen import WritePosition

from src.tuicub.game.widgets.frame import Frame


class TestFromWritePosition:
    def test_returns_frame_from_write_position(self) -> None:
        write_position = WritePosition(xpos=2, ypos=4, width=6, height=8)
        expected = Frame(x=2, y=4, width=6, height=8)

        result = Frame.from_write_position(write_position)

        assert result == expected


class TestToWritePosition:
    def test_returns_write_position_from_frame(self) -> None:
        expected = WritePosition(xpos=2, ypos=4, width=6, height=8)
        sut = Frame(x=2, y=4, width=6, height=8)

        result = sut.to_write_position()

        assert result.xpos == expected.xpos
        assert result.ypos == expected.ypos
        assert result.width == expected.width
        assert result.height == expected.height
