from src.tuicub.common.views import Color as UIColor
from src.tuicub.game.models import Color, Tile, Tileset


class TestColor:
    def test_ui_color__when_red__returns_tile_red(self) -> None:
        expected = UIColor.TILE_RED
        sut = Color.RED

        result = sut.ui_color

        assert result == expected

    def test_ui_color__when_yellow__returns_tile_yellow(self) -> None:
        expected = UIColor.TILE_YELLOW
        sut = Color.YELLOW

        result = sut.ui_color

        assert result == expected

    def test_ui_color__when_blue__returns_tile_blue(self) -> None:
        expected = UIColor.TILE_BLUE
        sut = Color.BLUE

        result = sut.ui_color

        assert result == expected

    def test_ui_color__when_black__returns_tile_black(self) -> None:
        expected = UIColor.TILE_BLACK
        sut = Color.BLACK

        result = sut.ui_color

        assert result == expected

    def test_ui_selected_color__when_red__returns_tile_red(self) -> None:
        expected = UIColor.TILE_RED
        sut = Color.RED

        result = sut.ui_selected_color

        assert result == expected

    def test_ui_selected_color__when_yellow__returns_tile_yellow(self) -> None:
        expected = UIColor.TILE_YELLOW
        sut = Color.YELLOW

        result = sut.ui_selected_color

        assert result == expected

    def test_ui_selected_color__when_blue__returns_tile_blue(self) -> None:
        expected = UIColor.TILE_BLUE
        sut = Color.BLUE

        result = sut.ui_selected_color

        assert result == expected

    def test_ui_selected_color__when_black__returns_tile_black_selected(self) -> None:
        expected = UIColor.TILE_BLACK_SELECTED
        sut = Color.BLACK

        result = sut.ui_selected_color

        assert result == expected


class TestTile:
    def test_str__returns_correct_string(self) -> None:
        expected = "[1] 2 RED(1)"
        sut = Tile.from_id(1)

        result = str(sut)

        assert result == expected


class TestTileset:
    def test_str__returns_correct_string(self) -> None:
        expected = "['[1] 2 RED(1)', '[2] 3 RED(1)', '[3] 4 RED(1)']"
        sut = Tileset(tiles=(Tile.from_id(1), Tile.from_id(2), Tile.from_id(3)))

        result = str(sut)

        assert result == expected
