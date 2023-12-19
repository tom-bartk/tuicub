from unittest.mock import Mock, PropertyMock, create_autospec, patch

import pytest
from prompt_toolkit.layout import to_container

from src.tuicub.common.screens import ScreenName
from src.tuicub.common.strings import GAMEROOM_USER_ROW_OWNER_BADGE
from src.tuicub.common.views import Color, Text, TextPart, TextView
from src.tuicub.common.views.text import EMPTY_TEXT
from src.tuicub.gameroom.keybinds import GameroomKeybindsContainer
from src.tuicub.gameroom.view import (
    GameroomPlayersListView,
    GameroomPlayersListViewHeader,
    GameroomScreen,
    GameroomView,
    UserRow,
    UserRowViewModel,
)
from src.tuicub.gameroom.viewmodel import GameroomViewModel


@pytest.fixture()
def list_view() -> GameroomPlayersListView:
    return create_autospec(GameroomPlayersListView)


@pytest.fixture()
def keybinds_container() -> GameroomKeybindsContainer:
    return create_autospec(GameroomKeybindsContainer)


@pytest.fixture()
def row_viewmodel() -> UserRowViewModel:
    return create_autospec(UserRowViewModel)


@pytest.fixture()
def viewmodel() -> GameroomViewModel:
    return create_autospec(GameroomViewModel)


class TestUserRowViewModel:
    def test_text__when_not_owner__returns_just_name(self, user_1) -> None:
        sut = UserRowViewModel(user=user_1, is_owner=False)
        expected = Text.plain(user_1.name, Color.FG0)

        result = sut.text()

        assert result == expected

    def test_text__when_is_owner__returns_name_with_owner_badge(self, user_1) -> None:
        sut = UserRowViewModel(user=user_1, is_owner=True)
        expected = Text(
            TextPart(user_1.name, Color.FG0),
            TextPart.flex(),
            TextPart(
                f" {GAMEROOM_USER_ROW_OWNER_BADGE} ",
                Color.BLUE,
                Color.BLUE_DIM,
                bold=True,
            ),
        )

        result = sut.text()

        assert result == expected

    def test_hash__returns_hash_of_user(self, user_1) -> None:
        sut = UserRowViewModel(user=user_1, is_owner=True)
        expected = hash(user_1)

        result = hash(sut)

        assert result == expected

    def test_eq__compares_instances_by_users(self, user_1) -> None:
        lhs = UserRowViewModel(user=user_1, is_owner=True)
        rhs = UserRowViewModel(user=user_1, is_owner=False)
        expected = True

        result = lhs == rhs

        assert result == expected


class TestUserRow:
    @pytest.fixture()
    def sut(self, row_viewmodel) -> UserRow:
        return UserRow(viewmodel=row_viewmodel)

    def test_viewmodel__returns_value_from_init(
        self, sut: UserRow, row_viewmodel
    ) -> None:
        expected = row_viewmodel

        result = sut.viewmodel

        assert result == expected

    def test_is_highlighted__returns_false(self, sut: UserRow) -> None:
        expected = False

        result = sut.is_highlighted

        assert result == expected

    def test_set_viewmodel__sets_text_to_value_from_viewmodel(self, sut: UserRow) -> None:
        new_viewmodel = create_autospec(UserRowViewModel)
        new_viewmodel.text = EMPTY_TEXT

        sut.viewmodel = new_viewmodel

        assert sut.text == new_viewmodel.text

    def test_eq__compares_viewmodel(self, gameroom_1) -> None:
        lhs = UserRow(viewmodel=UserRowViewModel(user=gameroom_1, is_owner=False))
        rhs = UserRow(viewmodel=UserRowViewModel(user=gameroom_1, is_owner=False))
        expected = True

        result = lhs == rhs

        assert result == expected

    def test_hash__hashes_viewmodel(self, user_1) -> None:
        viewmodel = UserRowViewModel(user=user_1, is_owner=False)
        sut = UserRow(viewmodel=viewmodel)
        expected = hash(viewmodel)

        result = hash(sut)

        assert result == expected


class TestGameroomPlayersListViewHeader:
    def test_focus_target__returns_logo_label(self) -> None:
        get_text = Mock(return_value=Text())
        sut = GameroomPlayersListViewHeader(get_text=get_text)
        expected = TextView(text=get_text)

        result = sut.focus_target()

        assert result == expected


class TestGameroomPlayersListView:
    def test_list_widget_rows__when_cache_misses__creates_new_rows(
        self, viewmodel, cache, user_1, user_2
    ) -> None:
        cache.get = Mock(return_value=None)
        vm1 = UserRowViewModel(user=user_1, is_owner=True)
        vm2 = UserRowViewModel(user=user_2, is_owner=False)
        viewmodel.rows = Mock(return_value=(vm1, vm2))
        expected = [UserRow(viewmodel=vm1), UserRow(viewmodel=vm2)]

        sut = GameroomPlayersListView(viewmodel=viewmodel, cache=cache)

        result = sut.list_widget.rows

        assert result == expected
        assert cache.set.call_count == 2

    def test_list_widget_rows__when_cache_hits__sets_row_viewmodels(
        self, viewmodel, cache, user_1, user_2
    ) -> None:
        cached_row1 = create_autospec(UserRow)
        mock_vm_prop1 = PropertyMock()
        type(cached_row1).viewmodel = mock_vm_prop1

        cached_row2 = create_autospec(UserRow)
        mock_vm_prop2 = PropertyMock()
        type(cached_row2).viewmodel = mock_vm_prop2

        cache.get = Mock(side_effect=[cached_row1, cached_row2])

        vm1 = UserRowViewModel(user=user_1, is_owner=True)
        vm2 = UserRowViewModel(user=user_2, is_owner=False)
        viewmodel.rows = Mock(return_value=(vm1, vm2))
        expected = [cached_row1, cached_row2]

        sut = GameroomPlayersListView(viewmodel=viewmodel, cache=cache)

        result = sut.list_widget.rows

        assert result == expected
        mock_vm_prop1.assert_called_once_with(vm1)
        mock_vm_prop2.assert_called_once_with(vm2)

    def test_list_header__returns_gamerooms_list_view_header_instance(
        self, viewmodel, cache
    ) -> None:
        sut = GameroomPlayersListView(viewmodel=viewmodel, cache=cache)

        result = sut.header

        assert isinstance(result, GameroomPlayersListViewHeader)


class TestGameroomView:
    @pytest.fixture()
    def sut(self, viewmodel, list_view, keybinds_container) -> GameroomView:
        return GameroomView(
            viewmodel=viewmodel,
            list_view=list_view,
            keybinds_container=keybinds_container,
        )

    def test_did_appear__subscribes_viewmodel(self, sut: GameroomView, viewmodel) -> None:
        with patch("prompt_toolkit.application.get_app"):
            sut.did_appear()

            viewmodel.subscribe.assert_called_once()

    def test_will_appear__unsubscribes_viewmodel(
        self, sut: GameroomView, viewmodel
    ) -> None:
        sut.will_disappear()

        viewmodel.unsubscribe.assert_called_once()

    def test_focus_target__returns_list_view_header_focus_target(
        self, sut: GameroomView, list_view
    ) -> None:
        expected = Mock()
        list_view.header.focus_target = Mock(return_value=expected)

        result = sut.focus_target()

        assert result == expected

    def test_keybinds_target__returns_list_view_list_widget(
        self, sut: GameroomView, list_view
    ) -> None:
        expected = Mock()
        list_view.list_widget = expected

        result = sut.keybinds_target()

        assert result == expected

    def test_pt_container__returns_list_view(self, sut: GameroomView, list_view) -> None:
        expected = list_view

        result = to_container(sut)

        assert result == expected


class TestGameroomScreen:
    @pytest.fixture()
    def sut(self, keybinds_container) -> GameroomScreen:
        view = create_autospec(GameroomView)
        return GameroomScreen(view=view, keybinds_container=keybinds_container)

    def test_screen_name__returns_gamerooms(self, sut: GameroomScreen) -> None:
        expected = ScreenName.GAMEROOM

        result = sut.screen_name

        assert result == expected
