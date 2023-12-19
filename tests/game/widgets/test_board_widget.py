from src.tuicub.game.widgets.base import Frame
from src.tuicub.game.widgets.board import BoardWidget
from src.tuicub.game.widgets.renderer import VerticalPosition
from src.tuicub.game.widgets.row import RowWidget


class TestRender:
    def test_renders_rows_vertically_centered(
        self, tileset_vm, tile_vm, theme, renderer, screen
    ) -> None:
        board = (
            (
                tileset_vm(tile_vm(1), tile_vm(2), tile_vm(3)),
                tileset_vm(tile_vm(4), tile_vm(5), tile_vm(6)),
            ),
            (tileset_vm(tile_vm(7), tile_vm(8), tile_vm(9)),),
        )
        rows: tuple[RowWidget, ...] = (
            RowWidget(
                tilesets=(
                    tileset_vm(tile_vm(1), tile_vm(2), tile_vm(3)),
                    tileset_vm(tile_vm(4), tile_vm(5), tile_vm(6)),
                ),
                theme=theme,
            ),
            RowWidget(
                tilesets=(tileset_vm(tile_vm(7), tile_vm(8), tile_vm(9)),),
                theme=theme,
            ),
        )
        frame = Frame(x=0, y=0, width=42, height=10)
        sut = BoardWidget(board=board, theme=theme)

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.render_vertically.assert_called_once_with(
            rows, VerticalPosition.CENTER, frame, screen, width=42
        )
