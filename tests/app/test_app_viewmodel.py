from collections.abc import Sequence
from unittest.mock import Mock, create_autospec

import pytest

from src.tuicub.app.state import AppState
from src.tuicub.app.status import StatusViewModel
from src.tuicub.app.viewmodel import AppViewModel, keybinds_text
from src.tuicub.common.models import Keybind
from src.tuicub.common.views import Color, Text, TextPart


@pytest.fixture()
def status_viewmodel() -> StatusViewModel:
    return create_autospec(StatusViewModel)


@pytest.fixture()
def global_keybinds() -> Sequence[Keybind]:
    return [Keybind("q", display_key="q", tooltip="quit", action=Mock())]


@pytest.fixture()
def sut(store, status_viewmodel, app_store, global_keybinds) -> AppViewModel:
    return AppViewModel(
        local_store=app_store,
        global_keybinds=global_keybinds,
        status_viewmodel=status_viewmodel,
    )


class TestKeybinds:
    def test_when_confirmation_none__returns_enabled_keybinds_text(
        self, sut, status_viewmodel, app_store
    ) -> None:
        keybinds = Mock(
            return_value=[
                Keybind("f", display_key="f", tooltip="foo", action=Mock()),
                Keybind("b", display_key="b", tooltip="bar", action=Mock()),
            ]
        )
        app_store.state = AppState(confirmation=None)
        expected = Text(
            TextPart("❬", fg=Color.BG7),
            TextPart("q", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG7),
            TextPart("quit", fg=Color.FG1),
            TextPart(" Ⅰ", Color.BG7),
            TextPart("❬", fg=Color.BG7),
            TextPart("f", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG7),
            TextPart("foo", fg=Color.FG1),
            TextPart(" Ⅰ", Color.BG7),
            TextPart("❬", fg=Color.BG7),
            TextPart("b", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG7),
            TextPart("bar", fg=Color.FG1),
        )

        sut.bind_keybinds(keybinds)
        result = sut.keybinds()

        assert result == expected

    def test_when_confirmation_not_none__returns_enabled_keybinds_text(
        self, sut, status_viewmodel, app_store
    ) -> None:
        keybinds = Mock(
            return_value=[
                Keybind("f", display_key="f", tooltip="foo", action=Mock()),
                Keybind("b", display_key="b", tooltip="bar", action=Mock()),
            ]
        )
        app_store.state = AppState(confirmation=Mock())
        expected = Text(
            TextPart("❬", fg=Color.BG5),
            TextPart("q", fg=Color.YELLOW_DIM, bold=True),
            TextPart("❭", fg=Color.BG5),
            TextPart("quit", fg=Color.FG5),
            TextPart(" Ⅰ", Color.BG5),
            TextPart("❬", fg=Color.BG5),
            TextPart("f", fg=Color.YELLOW_DIM, bold=True),
            TextPart("❭", fg=Color.BG5),
            TextPart("foo", fg=Color.FG5),
            TextPart(" Ⅰ", Color.BG5),
            TextPart("❬", fg=Color.BG5),
            TextPart("b", fg=Color.YELLOW_DIM, bold=True),
            TextPart("❭", fg=Color.BG5),
            TextPart("bar", fg=Color.FG5),
        )

        sut.bind_keybinds(keybinds)
        result = sut.keybinds()

        assert result == expected

    def test_when_keybind_condition_false__does_not_display_keybind(
        self, sut, status_viewmodel, app_store
    ) -> None:
        keybinds = Mock(
            return_value=[
                Keybind(
                    "f",
                    display_key="f",
                    tooltip="foo",
                    action=Mock(),
                    condition=Mock(return_value=False),
                ),
                Keybind("b", display_key="b", tooltip="bar", action=Mock()),
            ]
        )
        app_store.state = AppState(confirmation=None)
        expected = Text(
            TextPart("❬", fg=Color.BG7),
            TextPart("q", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG7),
            TextPart("quit", fg=Color.FG1),
            TextPart(" Ⅰ", Color.BG7),
            TextPart("❬", fg=Color.BG7),
            TextPart("b", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG7),
            TextPart("bar", fg=Color.FG1),
        )

        sut.bind_keybinds(keybinds)
        result = sut.keybinds()

        assert result == expected

    def test_when_keybind_hidden__does_not_display_keybind(
        self, sut, status_viewmodel, app_store
    ) -> None:
        keybinds = Mock(
            return_value=[
                Keybind(
                    "f", display_key="f", tooltip="foo", action=Mock(), is_hidden=True
                ),
                Keybind("b", display_key="b", tooltip="bar", action=Mock()),
            ]
        )
        app_store.state = AppState(confirmation=None)
        expected = Text(
            TextPart("❬", fg=Color.BG7),
            TextPart("q", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG7),
            TextPart("quit", fg=Color.FG1),
            TextPart(" Ⅰ", Color.BG7),
            TextPart("❬", fg=Color.BG7),
            TextPart("b", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG7),
            TextPart("bar", fg=Color.FG1),
        )

        sut.bind_keybinds(keybinds)
        result = sut.keybinds()

        assert result == expected


class TestOnAppState:
    def test_sets_confirmation_on_status_viewmodel(self, sut, status_viewmodel) -> None:
        confirmation = Mock()

        sut.on_state(AppState(confirmation=confirmation))

        status_viewmodel.set_confirmation.assert_called_once_with(
            confirmation=confirmation
        )


class TestSubscribe:
    def test_subscribes_to_app_store(self, sut, app_store) -> None:
        sut.subscribe()

        app_store.subscribe.assert_called_once_with(sut, include_current=True)


class TestUnsubscribe:
    def test_unsubscribes_from_app_store(self, sut, app_store) -> None:
        sut.unsubscribe()

        app_store.unsubscribe.assert_called_once_with(sut)


class TestKeybindsText:
    def test_when_enabled__returns_text_with_correct_colors(self) -> None:
        expected = Text(
            TextPart("❬", fg=Color.BG7),
            TextPart("a", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG7),
            TextPart("foo", fg=Color.FG1),
            TextPart(" Ⅰ", Color.BG7),
            TextPart("❬", fg=Color.BG7),
            TextPart("b", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG7),
            TextPart("bar", fg=Color.FG1),
        )

        result = keybinds_text(
            keybinds=(
                Keybind(key="a", display_key="a", tooltip="foo", action=Mock()),
                Keybind(key="b", display_key="b", tooltip="bar", action=Mock()),
            ),
            enabled=True,
        )

        assert result == expected

    def test_when_not_enabled__returns_text_with_correct_colors(self) -> None:
        expected = Text(
            TextPart("❬", fg=Color.BG5),
            TextPart("a", fg=Color.YELLOW_DIM, bold=True),
            TextPart("❭", fg=Color.BG5),
            TextPart("foo", fg=Color.FG5),
            TextPart(" Ⅰ", Color.BG5),
            TextPart("❬", fg=Color.BG5),
            TextPart("b", fg=Color.YELLOW_DIM, bold=True),
            TextPart("❭", fg=Color.BG5),
            TextPart("bar", fg=Color.FG5),
        )

        result = keybinds_text(
            keybinds=(
                Keybind(key="a", display_key="a", tooltip="foo", action=Mock()),
                Keybind(key="b", display_key="b", tooltip="bar", action=Mock()),
            ),
            enabled=False,
        )

        assert result == expected
