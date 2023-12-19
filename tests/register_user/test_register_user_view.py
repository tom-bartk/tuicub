from unittest.mock import create_autospec

import pytest
from prompt_toolkit.layout import to_container

from src.tuicub.common.screens import ScreenName
from src.tuicub.common.strings import (
    REGISTER_USER_BANNER,
    REGISTER_USER_HERO_TITLE,
    REGISTER_USER_TEXTFIELD_LABEL,
)
from src.tuicub.common.views import Color, Text, TextfieldView
from src.tuicub.register_user.keybinds import RegisterUserKeybindsContainer
from src.tuicub.register_user.view import (
    RegisterUserContent,
    RegisterUserScreen,
    RegisterUserView,
)
from tests.utils import all_texts


@pytest.fixture()
def content() -> RegisterUserContent:
    return create_autospec(RegisterUserContent)


@pytest.fixture()
def view() -> RegisterUserView:
    return create_autospec(RegisterUserView)


@pytest.fixture()
def keybinds_container() -> RegisterUserKeybindsContainer:
    return create_autospec(RegisterUserKeybindsContainer)


class TestRegisterUserView:
    @pytest.fixture()
    def sut(self, content, keybinds_container) -> RegisterUserView:
        return RegisterUserView(content=content, keybinds_container=keybinds_container)

    def test_focus_target__returns_content_textfield(self, sut, content) -> None:
        expected = content.textfield

        result = sut.focus_target()

        assert result == expected

    def test_keybinds_target__returns_content(self, sut, content) -> None:
        expected = content

        result = sut.keybinds_target()

        assert result == expected

    def test_pt_container__returns_content(self, sut, content) -> None:
        expected = content

        result = to_container(sut)

        assert result == expected


class TestRegisterUserContent:
    @pytest.fixture()
    def sut(self) -> RegisterUserContent:
        return RegisterUserContent()

    def test_contains_correct_text(self, sut: RegisterUserContent) -> None:
        expected = [
            Text.plain(REGISTER_USER_BANNER, Color.YELLOW),
            Text.plain(REGISTER_USER_HERO_TITLE, Color.FG1, bold=True),
            Text.plain(REGISTER_USER_TEXTFIELD_LABEL, Color.FG4),
        ]

        result: list[Text] = []
        all_texts(container=sut, current=result)

        assert result == expected

    def test_textfield__is_valid_textfield(self, sut: RegisterUserContent) -> None:
        result = sut.textfield

        assert isinstance(result, TextfieldView)


class TestRegisterUserScreen:
    @pytest.fixture()
    def sut(self, view, keybinds_container) -> RegisterUserScreen:
        return RegisterUserScreen(view=view, keybinds_container=keybinds_container)

    def test_screen_name__returns_register_user(self, sut: RegisterUserScreen) -> None:
        expected = ScreenName.REGISTER_USER

        result = sut.screen_name

        assert result == expected
