from unittest.mock import Mock, PropertyMock, create_autospec, patch

import pytest
from prompt_toolkit.layout import WindowAlign, to_container

from src.tuicub.common.screens import ScreenName
from src.tuicub.common.strings import (
    GAMEROOMS_EMPTY_STATE_SUBTITLE,
    GAMEROOMS_EMPTY_STATE_TITLE,
    GAMEROOMS_LIST_LABEL,
    GAMEROOMS_LOGO,
)
from src.tuicub.common.views import Color, Text, TextPart, TextView
from src.tuicub.common.views.text import EMPTY_TEXT
from src.tuicub.gamerooms.keybinds import GameroomsKeybindsContainer
from src.tuicub.gamerooms.view import (
    GameroomRow,
    GameroomRowViewModel,
    GameroomsListEmptyState,
    GameroomsListView,
    GameroomsListViewHeader,
    GameroomsScreen,
    GameroomsView,
)
from src.tuicub.gamerooms.viewmodel import GameroomsViewModel
from tests.utils import all_texts


@pytest.fixture()
def list_view() -> GameroomsListView:
    return create_autospec(GameroomsListView)


@pytest.fixture()
def keybinds_container() -> GameroomsKeybindsContainer:
    return create_autospec(GameroomsKeybindsContainer)


@pytest.fixture()
def row_viewmodel() -> GameroomRowViewModel:
    return create_autospec(GameroomRowViewModel)


@pytest.fixture()
def viewmodel() -> GameroomsViewModel:
    return create_autospec(GameroomsViewModel)


class TestGameroomRowViewModel:
    def test_is_highlighted__returns_value_from_init(self, gameroom) -> None:
        sut = GameroomRowViewModel(gameroom=gameroom, is_highlighted=True)
        expected = True

        result = sut.is_highlighted()

        assert result == expected

    def test_text__returns_gameroom_text(self, gameroom) -> None:
        sut = GameroomRowViewModel(gameroom=gameroom, is_highlighted=True)
        expected = Mock()

        with patch(
            "src.tuicub.common.views.gameroom.gameroom_text", return_value=expected
        ):
            result = sut.text()

            assert result == expected

    def test_text__calls_gameroom_text_with_gameroom_and_is_highlighted(
        self, gameroom
    ) -> None:
        sut = GameroomRowViewModel(gameroom=gameroom, is_highlighted=True)

        with patch(
            "src.tuicub.common.views.gameroom.gameroom_text"
        ) as mocked_gameroom_text:
            _ = sut.text()

            mocked_gameroom_text.assert_called_once_with(
                gameroom=gameroom, is_highlighted=True
            )

    def test_background_color__when_is_highlighted__returns_bg6(self, gameroom) -> None:
        sut = GameroomRowViewModel(gameroom=gameroom, is_highlighted=True)
        expected = Color.BG6

        result = sut.background_color()

        assert result == expected

    def test_background_color__when_not_highlighted__returns_bg3(self, gameroom) -> None:
        sut = GameroomRowViewModel(gameroom=gameroom, is_highlighted=False)
        expected = Color.BG3

        result = sut.background_color()

        assert result == expected

    def test_with_is_highlighted__returns_copy_with_updated_is_highlighted(
        self, gameroom
    ) -> None:
        sut = GameroomRowViewModel(gameroom=gameroom, is_highlighted=False)
        expected = GameroomRowViewModel(gameroom=gameroom, is_highlighted=True)

        result = sut.with_is_highlighted(is_highlighted=True)

        assert result == expected

    def test_hash__returns_hash_of_gameroom(self, gameroom) -> None:
        sut = GameroomRowViewModel(gameroom=gameroom, is_highlighted=False)
        expected = hash(gameroom)

        result = hash(sut)

        assert result == expected

    def test_eq__compares_instances_by_gamerooms(self, gameroom) -> None:
        lhs = GameroomRowViewModel(gameroom=gameroom, is_highlighted=False)
        rhs = GameroomRowViewModel(gameroom=gameroom, is_highlighted=True)
        expected = True

        result = lhs == rhs

        assert result == expected


class TestGameroomRow:
    @pytest.fixture()
    def sut(self, row_viewmodel) -> GameroomRow:
        return GameroomRow(viewmodel=row_viewmodel)

    def test_viewmodel__returns_value_from_init(
        self, sut: GameroomRow, row_viewmodel
    ) -> None:
        expected = row_viewmodel

        result = sut.viewmodel

        assert result == expected

    def test_is_highlighted__returns_viewmodel_value(
        self, sut: GameroomRow, row_viewmodel
    ) -> None:
        row_viewmodel.is_highlighted.return_value = True
        expected = True

        result = sut.is_highlighted

        assert result == expected
        row_viewmodel.is_highlighted.assert_called_once()

    def test_set_viewmodel__sets_text_and_background_color_to_values_from_viewmodel(
        self, sut: GameroomRow
    ) -> None:
        new_viewmodel = create_autospec(GameroomRowViewModel)
        new_viewmodel.text = EMPTY_TEXT
        new_viewmodel.background_color = Mock()

        sut.viewmodel = new_viewmodel

        assert sut.text == new_viewmodel.text
        assert sut.background_color == new_viewmodel.background_color

    def test_eq__compares_viewmodel_and_is_highlighted(self, gameroom) -> None:
        lhs = GameroomRow(
            viewmodel=GameroomRowViewModel(gameroom=gameroom, is_highlighted=False)
        )
        rhs = GameroomRow(
            viewmodel=GameroomRowViewModel(gameroom=gameroom, is_highlighted=False)
        )
        expected = True

        result = lhs == rhs

        assert result == expected

    def test_hash__hashes_viewmodel(self, gameroom) -> None:
        viewmodel = GameroomRowViewModel(gameroom=gameroom, is_highlighted=False)
        sut = GameroomRow(viewmodel=viewmodel)
        expected = hash(viewmodel)

        result = hash(sut)

        assert result == expected


class TestGameroomsListEmptyState:
    def test_text__returns_correct_text(self) -> None:
        sut = GameroomsListEmptyState()
        expected = Text(
            TextPart(GAMEROOMS_EMPTY_STATE_TITLE, Color.FG1, bold=True),
            TextPart(GAMEROOMS_EMPTY_STATE_SUBTITLE, Color.FG4),
            TextPart("❬", Color.BG8),
            TextPart("c", Color.YELLOW, bold=True),
            TextPart("❭", Color.BG8),
            TextPart("."),
        )

        result = sut.text

        assert result == expected


class TestGameroomsListViewHeader:
    def test_when_list_empty__has_logo_and_empty_state(self) -> None:
        sut = GameroomsListViewHeader(is_list_empty=Mock(return_value=True))
        expected = [
            Text.plain(GAMEROOMS_LOGO, Color.YELLOW),
            Text(
                TextPart(GAMEROOMS_EMPTY_STATE_TITLE, Color.FG1, bold=True),
                TextPart(GAMEROOMS_EMPTY_STATE_SUBTITLE, Color.FG4),
                TextPart("❬", Color.BG8),
                TextPart("c", Color.YELLOW, bold=True),
                TextPart("❭", Color.BG8),
                TextPart("."),
            ),
        ]

        result: list[Text] = []
        all_texts(container=sut, current=result)

        assert result == expected

    def test_when_list_not_empty__has_logo_and_list_label(self) -> None:
        sut = GameroomsListViewHeader(is_list_empty=Mock(return_value=False))
        expected = [
            Text.plain(GAMEROOMS_LOGO, Color.YELLOW),
            Text.plain(GAMEROOMS_LIST_LABEL, Color.FG5, bold=True),
        ]

        result: list[Text] = []
        all_texts(container=sut, current=result)

        assert result == expected

    def test_focus_target__returns_logo_label(self) -> None:
        sut = GameroomsListViewHeader(is_list_empty=Mock(return_value=True))
        expected = TextView.plain(GAMEROOMS_LOGO, Color.YELLOW, WindowAlign.CENTER)

        result = sut.focus_target()

        assert result == expected


class TestGameroomsListView:
    def test_list_widget_rows__when_cache_misses__creates_new_rows(
        self, viewmodel, cache, gameroom_1, gameroom_2
    ) -> None:
        cache.get = Mock(return_value=None)
        vm1 = GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=True)
        vm2 = GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=False)
        viewmodel.rows = Mock(return_value=(vm1, vm2))
        expected = [GameroomRow(viewmodel=vm1), GameroomRow(viewmodel=vm2)]

        sut = GameroomsListView(viewmodel=viewmodel, cache=cache)

        result = sut.list_widget.rows

        assert result == expected
        assert cache.set.call_count == 2

    def test_list_widget_rows__when_cache_hits__sets_row_viewmodels(
        self, viewmodel, cache, gameroom_1, gameroom_2
    ) -> None:
        cached_row1 = create_autospec(GameroomRow)
        mock_vm_prop1 = PropertyMock()
        type(cached_row1).viewmodel = mock_vm_prop1

        cached_row2 = create_autospec(GameroomRow)
        mock_vm_prop2 = PropertyMock()
        type(cached_row2).viewmodel = mock_vm_prop2

        cache.get = Mock(side_effect=[cached_row1, cached_row2])

        vm1 = GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=True)
        vm2 = GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=False)
        viewmodel.rows = Mock(return_value=(vm1, vm2))
        expected = [cached_row1, cached_row2]

        sut = GameroomsListView(viewmodel=viewmodel, cache=cache)

        result = sut.list_widget.rows

        assert result == expected
        mock_vm_prop1.assert_called_once_with(vm1)
        mock_vm_prop2.assert_called_once_with(vm2)

    def test_list_header__returns_gamerooms_list_view_header_instance(
        self, viewmodel, cache
    ) -> None:
        sut = GameroomsListView(viewmodel=viewmodel, cache=cache)

        result = sut.header

        assert isinstance(result, GameroomsListViewHeader)


class TestGameroomsView:
    @pytest.fixture()
    def sut(self, viewmodel, list_view, keybinds_container) -> GameroomsView:
        return GameroomsView(
            viewmodel=viewmodel,
            list_view=list_view,
            keybinds_container=keybinds_container,
        )

    def test_did_appear__subscribes_viewmodel(
        self, sut: GameroomsView, viewmodel
    ) -> None:
        with patch("prompt_toolkit.application.get_app"):
            sut.did_appear()

            viewmodel.subscribe.assert_called_once()

    def test_will_appear__unsubscribes_viewmodel(
        self, sut: GameroomsView, viewmodel
    ) -> None:
        sut.will_disappear()

        viewmodel.unsubscribe.assert_called_once()

    def test_focus_target__returns_list_view_header_focus_target(
        self, sut: GameroomsView, list_view
    ) -> None:
        expected = Mock()
        list_view.header.focus_target = Mock(return_value=expected)

        result = sut.focus_target()

        assert result == expected

    def test_keybinds_target__returns_list_view_list_widget(
        self, sut: GameroomsView, list_view
    ) -> None:
        expected = Mock()
        list_view.list_widget = expected

        result = sut.keybinds_target()

        assert result == expected

    def test_pt_container__returns_list_view(self, sut: GameroomsView, list_view) -> None:
        expected = list_view

        result = to_container(sut)

        assert result == expected


class TestGameroomsScreen:
    @pytest.fixture()
    def sut(self, keybinds_container) -> GameroomsScreen:
        view = create_autospec(GameroomsView)
        return GameroomsScreen(view=view, keybinds_container=keybinds_container)

    def test_screen_name__returns_gamerooms(self, sut: GameroomsScreen) -> None:
        expected = ScreenName.GAMEROOMS

        result = sut.screen_name

        assert result == expected
