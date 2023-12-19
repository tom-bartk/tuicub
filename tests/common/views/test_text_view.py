from unittest.mock import Mock

from src.tuicub.common.views.textview import TextView


class TestHash:
    def test_returns_hash_of_test_background_color_align_and_height(self) -> None:
        text = Mock()
        background_color = Mock()
        align = Mock()
        height = Mock()
        sut = TextView(
            text=text, background_color=background_color, align=align, height=height
        )
        expected = hash((text, background_color, align, height))

        result = hash(sut)

        assert result == expected
