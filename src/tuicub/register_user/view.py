from typing import Any

from prompt_toolkit.layout import AnyContainer, WindowAlign
from prompt_toolkit.layout.layout import FocusableElement

from ..common.screens import KeybindableElement, RootScreenView, ScreenName, TuicubScreen
from ..common.strings import (
    REGISTER_USER_BANNER,
    REGISTER_USER_HERO_TITLE,
    REGISTER_USER_TEXTFIELD_LABEL,
)
from ..common.views import (
    Color,
    HCenterView,
    Padding,
    StackView,
    TextfieldView,
    TextView,
    Theme,
    VCenterView,
)

CARD_HEIGHT = 10
CARD_PADDING = Padding(left=4, right=4, top=2, bottom=2)
CONTENT_WIDTH = 52
CONTENT_HEIGHT = 18


class RegisterUserContent(HCenterView):
    """The content of the register user screen."""

    @property
    def textfield(self) -> TextfieldView:
        """The user name textfield."""
        return self._textfield

    def __init__(self, theme: Theme | None = None) -> None:
        self._textfield: TextfieldView = TextfieldView(theme=theme)
        super().__init__(
            VCenterView(
                StackView.with_subviews(
                    TextView.plain(
                        REGISTER_USER_BANNER,
                        Color.YELLOW,
                        WindowAlign.CENTER,
                        theme=theme,
                    ),
                    StackView.with_subviews(
                        TextView.plain(
                            REGISTER_USER_HERO_TITLE,
                            Color.FG1,
                            WindowAlign.CENTER,
                            bold=True,
                            theme=theme,
                        ),
                        TextView.plain(
                            REGISTER_USER_TEXTFIELD_LABEL, Color.FG4, theme=theme
                        ),
                        self._textfield,
                        background_color=Color.BG4,
                        height=CARD_HEIGHT,
                        padding=CARD_PADDING,
                        theme=theme,
                    ),
                ),
                content_height=CONTENT_HEIGHT,
                theme=theme,
            ),
            content_width=CONTENT_WIDTH,
            theme=theme,
        )


class RegisterUserView(RootScreenView):
    """The root view of the register user screen."""

    __slots__ = ("_content",)

    def __init__(self, content: RegisterUserContent, *args: Any, **kwargs: Any):
        """Initialize new view.

        Args:
            content (RegisterUserContent): The content of the view.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.
        """
        self._content: RegisterUserContent = content
        super().__init__(*args, **kwargs)

    def focus_target(self) -> FocusableElement:
        return self._content.textfield

    def keybinds_target(self) -> KeybindableElement:
        return self._content

    def __pt_container__(self) -> AnyContainer:
        return self._content


class RegisterUserScreen(TuicubScreen[RegisterUserView]):
    __slots__ = ()

    @property
    def screen_name(self) -> str:
        return ScreenName.REGISTER_USER
