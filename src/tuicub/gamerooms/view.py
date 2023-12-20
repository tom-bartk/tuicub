from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from prompt_toolkit.layout import AnyContainer, Container, WindowAlign
from prompt_toolkit.layout.layout import FocusableElement

from ..common.cache import Cache
from ..common.models import Gameroom
from ..common.screens import KeybindableElement, RootScreenView, ScreenName, TuicubScreen
from ..common.strings import (
    GAMEROOMS_EMPTY_STATE_SUBTITLE,
    GAMEROOMS_EMPTY_STATE_TITLE,
    GAMEROOMS_LIST_LABEL,
    GAMEROOMS_LOGO,
)
from ..common.views import (
    Color,
    HCenterView,
    ListRow,
    ListView,
    Padding,
    SeparatorView,
    StackView,
    Text,
    TextPart,
    TextView,
    Theme,
    gameroom,
)

if TYPE_CHECKING:
    from .viewmodel import GameroomsViewModel

CONTENT_WIDTH = 80
LIST_PADDING = Padding.horizontal(2)


class GameroomRowViewModel:
    """The viewmodel of a gameroom list row."""

    __slots__ = ("_gameroom", "_is_highlighted")

    def __init__(self, gameroom: Gameroom, is_highlighted: bool):
        """Initialize new viewmodel.

        Args:
            gameroom (Gameroom): The gameroom of the row.
            is_highlighted (bool): Whether the current row is highlighted.
        """
        self._gameroom: Gameroom = gameroom
        self._is_highlighted: bool = is_highlighted

    def text(self) -> Text:
        return gameroom.gameroom_text(
            gameroom=self._gameroom, is_highlighted=self._is_highlighted
        )

    def is_highlighted(self) -> bool:
        return self._is_highlighted

    def background_color(self) -> Color:
        return Color.BG6 if self._is_highlighted else Color.BG3

    def with_is_highlighted(self, is_highlighted: bool) -> GameroomRowViewModel:
        return GameroomRowViewModel(
            gameroom=self._gameroom, is_highlighted=is_highlighted
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameroomRowViewModel):
            return NotImplemented

        return self._gameroom == other._gameroom

    def __hash__(self) -> int:
        return hash(self._gameroom)


class GameroomRow(ListRow):
    """The row of the gamerooms list."""

    @property
    def viewmodel(self) -> GameroomRowViewModel:
        return self._viewmodel

    @viewmodel.setter
    def viewmodel(self, new: GameroomRowViewModel) -> None:
        self._viewmodel: GameroomRowViewModel = new
        self.text = new.text
        self.background_color = new.background_color

    @property
    def is_highlighted(self) -> bool:
        return self._viewmodel.is_highlighted()

    def __init__(self, viewmodel: GameroomRowViewModel, theme: Theme | None = None):
        """Initialize new row.

        Args:
            viewmodel (GameroomRowViewModel): The viewmodel of the row.
            theme (Theme): The color theme.
        """
        self._viewmodel = viewmodel
        super().__init__(
            text=viewmodel.text, background_color=viewmodel.background_color, theme=theme
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameroomRow):
            return NotImplemented

        return (
            self.viewmodel == other.viewmodel
            and self.is_highlighted == other.is_highlighted
        )

    def __hash__(self) -> int:
        return hash(self._viewmodel)


class GameroomsListEmptyState(TextView):
    """The empty state view of the list."""

    def __init__(self, theme: Theme | None = None):
        super().__init__(
            Text(
                TextPart(GAMEROOMS_EMPTY_STATE_TITLE, Color.FG1, bold=True),
                TextPart(GAMEROOMS_EMPTY_STATE_SUBTITLE, Color.FG4),
                TextPart("❬", Color.BG8),
                TextPart("c", Color.YELLOW, bold=True),
                TextPart("❭", Color.BG8),
                TextPart("."),
            ),
            align=WindowAlign.CENTER,
            theme=theme,
        )


class GameroomsListViewHeader(StackView):
    """The header view of the list."""

    def __init__(self, is_list_empty: Callable[[], bool], theme: Theme | None = None):
        self._is_list_empty: Callable[[], bool] = is_list_empty
        self._logo_label = TextView.plain(
            GAMEROOMS_LOGO, Color.YELLOW, WindowAlign.CENTER, theme=theme
        )
        self._table_header_label = TextView.plain(
            GAMEROOMS_LIST_LABEL, Color.FG5, bold=True, theme=theme
        )
        self._empty_state = GameroomsListEmptyState(theme=theme)
        self._separator_view = SeparatorView(theme=theme)
        self._list_header = StackView(
            self._header_children,
            width=CONTENT_WIDTH,
            dont_extend_height=True,
            theme=theme,
        )
        super().__init__(
            self._header_children,
            width=CONTENT_WIDTH,
            dont_extend_height=True,
            theme=theme,
        )

    def _header_children(self) -> Sequence[Container]:
        if self._is_list_empty():
            return [self._logo_label, self._separator_view, self._empty_state]
        else:
            return [self._logo_label, self._separator_view, self._table_header_label]

    def focus_target(self) -> FocusableElement:
        return self._logo_label


class GameroomsListView(HCenterView):
    """The gamerooms list view."""

    @property
    def header(self) -> GameroomsListViewHeader:
        return self._header

    @property
    def list_widget(self) -> ListView:
        return self._list_view

    def __init__(
        self, viewmodel: GameroomsViewModel, cache: Cache, theme: Theme | None = None
    ):
        self._cache: Cache = cache
        self._theme: Theme = theme or Theme.default()
        self._viewmodel = viewmodel
        self._header = GameroomsListViewHeader(
            is_list_empty=viewmodel.is_list_empty, theme=theme
        )
        self._list_view = ListView(
            get_rows=self._get_rows,
            header=self._header,
            background_color=Color.BG3,
            padding=LIST_PADDING,
            theme=theme,
        )
        super().__init__(
            content=self._list_view, content_width=CONTENT_WIDTH, theme=theme
        )

    def _get_rows(self) -> Sequence[ListRow]:
        return [self._create_row(vm) for vm in self._viewmodel.rows()]

    def _create_row(self, viewmodel: GameroomRowViewModel) -> GameroomRow:
        if cached := self._cache.get(hash(viewmodel)):
            cached.viewmodel = viewmodel
            return cached

        row = GameroomRow(viewmodel, theme=self._theme)
        self._cache.set(key=hash(viewmodel), value=row)
        return row


class GameroomsView(RootScreenView):
    """The root view of the gamerooms screen."""

    __slots__ = ("_viewmodel", "_list_view")

    def __init__(
        self,
        viewmodel: GameroomsViewModel,
        list_view: GameroomsListView,
        *args: Any,
        **kwargs: Any,
    ):
        self._viewmodel = viewmodel
        self._list_view: GameroomsListView = list_view
        super().__init__(*args, **kwargs)

    def did_appear(self) -> None:
        super().did_appear()
        self._viewmodel.subscribe()

    def will_disappear(self) -> None:
        super().will_disappear()
        self._viewmodel.unsubscribe()

    def focus_target(self) -> FocusableElement:
        return self._list_view.header.focus_target()

    def keybinds_target(self) -> KeybindableElement:
        return self._list_view.list_widget

    def __pt_container__(self) -> AnyContainer:
        return self._list_view


class GameroomsScreen(TuicubScreen[GameroomsView]):
    __slots__ = ()

    @property
    def screen_name(self) -> str:
        return ScreenName.GAMEROOMS
