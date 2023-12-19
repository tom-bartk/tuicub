from unittest.mock import Mock, create_autospec, patch

import pytest
from prompt_toolkit.layout import DummyControl, Window

from src.tuicub.app.status import StatusView
from src.tuicub.app.view import AppView
from src.tuicub.app.viewmodel import AppViewModel
from src.tuicub.common.screens import TuicubScreen


@pytest.fixture()
def viewmodel() -> AppViewModel:
    return create_autospec(AppViewModel)


@pytest.fixture()
def status_view() -> StatusView:
    view = create_autospec(StatusView)
    view.__pt_container__ = Mock(return_value=Window(DummyControl()))
    return view


@pytest.fixture()
def initial_screen() -> TuicubScreen:
    screen = create_autospec(TuicubScreen)
    screen.__pt_container__ = Mock(return_value=Window(DummyControl()))
    return screen


@pytest.fixture()
def sut(viewmodel, status_view, initial_screen, theme) -> AppView:
    return AppView(
        viewmodel=viewmodel,
        status_view=status_view,
        initial_screen=initial_screen,
        theme=theme,
    )


class TestPresent:
    def test_binds_screen_keybinds_to_viewmodel(self, sut, viewmodel) -> None:
        viewmodel.reset_mock()
        keybinds = Mock()
        screen = create_autospec(TuicubScreen)
        screen.keybinds = keybinds

        with patch("prompt_toolkit.application.get_app"):
            sut.present(screen)

            viewmodel.bind_keybinds.assert_called_once_with(keybinds)

    def test_updates_current_screen(self, sut, viewmodel) -> None:
        screen = create_autospec(TuicubScreen)

        with patch("prompt_toolkit.application.get_app"):
            sut.present(screen)

            result = sut.screen()

            assert result == screen
