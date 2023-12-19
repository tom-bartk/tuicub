from unittest.mock import Mock, create_autospec, patch

import pytest
from prompt_toolkit.layout import to_container
from prompt_toolkit.layout.screen import WritePosition

from src.tuicub.common.screens import ScreenName
from src.tuicub.common.views import FocusWindow
from src.tuicub.game.keybinds import GameKeybindsContainer
from src.tuicub.game.view import GameRootView, GameScreen, GameView, GameWidgetFactory
from src.tuicub.game.viewmodel import GameViewModel
from src.tuicub.game.widgets.frame import Frame
from src.tuicub.game.widgets.game import GameWidget


@pytest.fixture()
def factory() -> GameWidgetFactory:
    return create_autospec(GameWidgetFactory)


@pytest.fixture()
def game_root_view() -> GameRootView:
    return create_autospec(GameRootView)


@pytest.fixture()
def focus_window() -> FocusWindow:
    return create_autospec(FocusWindow)


@pytest.fixture()
def view() -> GameView:
    return create_autospec(GameView)


@pytest.fixture()
def viewmodel() -> GameViewModel:
    return create_autospec(GameViewModel)


@pytest.fixture()
def keybinds_container() -> GameKeybindsContainer:
    return create_autospec(GameKeybindsContainer)


class TestGameView:
    @pytest.fixture()
    def sut(self, game_root_view, keybinds_container, renderer, viewmodel) -> GameView:
        return GameView(
            viewmodel=viewmodel,
            game_root_view=game_root_view,
            keybinds_container=keybinds_container,
        )

    def test_focus_target__returns_game_root_view_focus_target(
        self, sut, game_root_view
    ) -> None:
        expected = game_root_view.focus_target()

        result = sut.focus_target()

        assert result == expected

    def test_keybinds_target__returns_game_root_view(self, sut, game_root_view) -> None:
        expected = game_root_view

        result = sut.keybinds_target()

        assert result == expected

    def test_did_appear__subscribes_viewmodel(self, sut: GameView, viewmodel) -> None:
        with patch("prompt_toolkit.application.get_app"):
            sut.did_appear()

            viewmodel.subscribe.assert_called_once()

    def test_will_appear__unsubscribes_viewmodel(self, sut: GameView, viewmodel) -> None:
        sut.will_disappear()

        viewmodel.unsubscribe.assert_called_once()

    def test_pt_container__returns_game_root_view(
        self, sut: GameView, game_root_view
    ) -> None:
        expected = game_root_view

        result = to_container(sut)

        assert result == expected


class TestGameWidgetFactory:
    @pytest.fixture()
    def sut(self, viewmodel) -> GameWidgetFactory:
        return GameWidgetFactory(viewmodel=viewmodel)

    def test_create__returns_game_widget(self, sut: GameWidgetFactory, viewmodel) -> None:
        expected = GameWidget(
            board=viewmodel.board,
            rack=viewmodel.rack,
            pile=viewmodel.pile,
            players=viewmodel.players,
            status_bar=viewmodel.status_bar,
            winner=viewmodel.winner,
        )

        result = sut.create()

        assert result == expected


class TestGameRootView:
    @pytest.fixture()
    def sut(self, factory, focus_window, renderer) -> GameRootView:
        return GameRootView(factory=factory, focus_window=focus_window, renderer=renderer)

    def test_get_children__returns_focus_window(
        self, sut: GameRootView, focus_window
    ) -> None:
        expected = [focus_window]

        result = sut.get_children()

        assert result == expected

    def test_get_key_bindings__returns_focus_window_control_key_bindings(
        self, sut: GameRootView, focus_window
    ) -> None:
        expected = Mock()
        focus_window.control.get_key_bindings.return_value = expected

        result = sut.get_key_bindings()

        assert result == expected

    def test_focus_target__returns_focus_window(
        self, sut: GameRootView, focus_window
    ) -> None:
        expected = focus_window

        result = sut.focus_target()

        assert result == expected

    def test_key_bindings__returns_focus_window_control_key_bindings(
        self, sut: GameRootView, focus_window
    ) -> None:
        expected = focus_window
        focus_window.control.key_bindings = expected

        result = sut.key_bindings

        assert result == expected

    def test_key_bindings_setter__sets_focus_window_control_key_bindings(
        self, sut: GameRootView, focus_window
    ) -> None:
        key_bindings = Mock()

        sut.key_bindings = key_bindings

        assert focus_window.control.key_bindings == key_bindings

    def test_write_to_screen__renders_game_widget_created_by_factory(
        self, sut: GameRootView, focus_window, renderer, screen, factory
    ) -> None:
        game_widget = create_autospec(GameWidget)
        factory.create.return_value = game_widget
        screen.height = 50

        sut.write_to_screen(
            screen=screen,
            mouse_handlers=Mock(),
            write_position=WritePosition(xpos=0, ypos=0, width=10, height=10),
            parent_style="",
            erase_bg=False,
            z_index=0,
        )

        game_widget.render.assert_called_once_with(
            renderer=renderer, screen=screen, frame=Frame(x=0, y=0, width=10, height=10)
        )


class TestGameScreen:
    @pytest.fixture()
    def sut(self, view, keybinds_container) -> GameScreen:
        return GameScreen(view=view, keybinds_container=keybinds_container)

    def test_screen_name__returns_register_user(self, sut: GameScreen) -> None:
        expected = ScreenName.GAME

        result = sut.screen_name

        assert result == expected
