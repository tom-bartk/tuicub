from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from prompt_toolkit.layout import AnyContainer
from prompt_toolkit.layout.layout import FocusableElement

from ..common.cache import Cache
from ..common.models import User
from ..common.screens import KeybindableElement, RootScreenView, ScreenName, TuicubScreen
from ..common.strings import GAMEROOM_LIST_LABEL, GAMEROOM_USER_ROW_OWNER_BADGE
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
)

if TYPE_CHECKING:
    from .viewmodel import GameroomViewModel

CONTENT_WIDTH = 80


class UserRowViewModel:
    """The viewmodel of a user list row."""

    __slots__ = ("_user", "_is_owner")

    def __init__(self, user: User, is_owner: bool):
        """Initialize new viewmodel.

        Args:
            user (User): The user to display.
            is_owner (bool): Whether the user owns the gameroom.
        """
        self._user: User = user
        self._is_owner: bool = is_owner

    def text(self) -> Text:
        if self._is_owner:
            return Text(
                TextPart(self._user.name, Color.FG0),
                TextPart.flex(),
                TextPart(
                    f" {GAMEROOM_USER_ROW_OWNER_BADGE} ",
                    Color.BLUE,
                    Color.BLUE_DIM,
                    bold=True,
                ),
            )
        return Text.plain(self._user.name, Color.FG0)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserRowViewModel):
            return NotImplemented

        return self._user == other._user

    def __hash__(self) -> int:
        return hash(self._user)


class UserRow(ListRow):
    """The row view of the list of users."""

    @property
    def viewmodel(self) -> UserRowViewModel:
        return self._viewmodel

    @viewmodel.setter
    def viewmodel(self, new: UserRowViewModel) -> None:
        self._viewmodel: UserRowViewModel = new
        self.text = new.text

    @property
    def is_highlighted(self) -> bool:
        return False

    def __init__(self, viewmodel: UserRowViewModel, theme: Theme | None = None):
        self._viewmodel = viewmodel
        super().__init__(text=viewmodel.text, height=2, theme=theme)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserRow):
            return NotImplemented

        return self.viewmodel == other.viewmodel

    def __hash__(self) -> int:
        return hash(self._viewmodel)


class GameroomPlayersListViewHeader(StackView):
    """The header view of the users list."""

    def __init__(self, get_text: Callable[[], Text], theme: Theme | None = None):
        self._gameroom_view: TextView = TextView(text=get_text, theme=theme)
        super().__init__(
            lambda: [
                self._gameroom_view,
                SeparatorView(theme=theme),
                TextView.plain(GAMEROOM_LIST_LABEL, Color.FG5, bold=True, theme=theme),
            ],
            width=CONTENT_WIDTH,
            dont_extend_height=True,
            theme=theme,
        )

    def focus_target(self) -> FocusableElement:
        return self._gameroom_view


class GameroomPlayersListView(HCenterView):
    """The users list view."""

    @property
    def header(self) -> GameroomPlayersListViewHeader:
        return self._header

    @property
    def list_widget(self) -> ListView:
        return self._list_view

    def __init__(
        self, viewmodel: GameroomViewModel, cache: Cache, theme: Theme | None = None
    ):
        self._cache: Cache = cache
        self._theme: Theme = theme or Theme.default()
        self._viewmodel = viewmodel
        self._header = GameroomPlayersListViewHeader(
            get_text=viewmodel.gameroom_text, theme=theme
        )
        self._list_view = ListView(
            get_rows=self._get_rows,
            header=self._header,
            background_color=Color.BG3,
            padding=Padding(left=2, right=2, top=2, bottom=0),
            theme=theme,
        )
        super().__init__(
            content=self._list_view, content_width=CONTENT_WIDTH, theme=theme
        )

    def _get_rows(self) -> Sequence[ListRow]:
        return [self._create_row(vm) for vm in self._viewmodel.rows()]

    def _create_row(self, viewmodel: UserRowViewModel) -> UserRow:
        if cached := self._cache.get(hash(viewmodel)):
            cached.viewmodel = viewmodel
            return cached

        row = UserRow(viewmodel, theme=self._theme)
        self._cache.set(key=hash(viewmodel), value=row)
        return row


class GameroomView(RootScreenView):
    """The root view of the gameroom screen."""

    __slots__ = ("_viewmodel", "_list_view")

    def __init__(
        self,
        viewmodel: GameroomViewModel,
        list_view: GameroomPlayersListView,
        *args: Any,
        **kwargs: Any,
    ):
        self._viewmodel = viewmodel
        self._list_view: GameroomPlayersListView = list_view
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


class GameroomScreen(TuicubScreen[GameroomView]):
    __slots__ = ()

    @property
    def screen_name(self) -> str:
        return ScreenName.GAMEROOM
