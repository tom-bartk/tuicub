from prompt_toolkit.renderer import Output


class ScreenSizeService:
    """A service for getting the size of the screen."""

    __slots__ = ("_output",)

    def __init__(self, output: Output):
        self._output: Output = output

    def width(self) -> int:
        """Returns the current width of the screen in characters."""
        return self._output.get_size().columns
