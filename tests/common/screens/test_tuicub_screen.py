from unittest.mock import create_autospec

import pytest

from src.tuicub.common.keybinds.container import KeybindsContainer
from src.tuicub.common.screens import (
    RootScreenView,
    ScreenLifecycleDelegate,
    TuicubScreen,
)


@pytest.fixture()
def view() -> RootScreenView:
    return create_autospec(RootScreenView)


@pytest.fixture()
def keybinds_container() -> KeybindsContainer:
    return create_autospec(KeybindsContainer)


@pytest.fixture()
def delegate() -> ScreenLifecycleDelegate:
    return create_autospec(ScreenLifecycleDelegate)


class MockScreen(TuicubScreen):
    @property
    def screen_name(self) -> str:
        return "foo"


@pytest.fixture()
def sut(view, keybinds_container) -> MockScreen:
    return MockScreen(view=view, keybinds_container=keybinds_container)


class TestDidPresent:
    def test_when_has_delegate__calls_screen_did_present_on_it(
        self, sut, delegate
    ) -> None:
        sut.set_delegate(delegate)
        sut.did_present()

        delegate.screen_did_present.assert_called_once_with(sut)

    def test_calls_did_appear_on_view(self, sut, view) -> None:
        sut.did_present()

        view.did_appear.assert_called_once()


class TestWillPresent:
    def test_calls_will_appear_on_view(self, sut, view) -> None:
        sut.will_present()

        view.will_appear.assert_called_once()


class TestWillDisappear:
    def test_calls_will_disappear_on_view(self, sut, view) -> None:
        sut.will_disappear()

        view.will_disappear.assert_called_once()


class TestPtContainer:
    def test_returns_view(self, sut, view) -> None:
        expected = view

        result = sut.__pt_container__()

        assert result == expected


class TestKeybinds:
    def test_returns_container_keybinds(self, sut, keybinds_container) -> None:
        expected = keybinds_container.keybinds()

        result = sut.keybinds()

        assert result == expected
