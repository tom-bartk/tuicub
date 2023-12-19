from unittest.mock import Mock, create_autospec, patch
from weakref import WeakMethod

import pytest

from src.tuicub.app.status import StatusView, StatusViewModel
from src.tuicub.common.confirmation import Confirmation
from src.tuicub.common.models import Alert
from src.tuicub.common.views import Color
from src.tuicub.common.views.animation import TextAnimator
from src.tuicub.common.views.text import EMPTY_TEXT


@pytest.fixture()
def animator() -> TextAnimator:
    return create_autospec(TextAnimator)


@pytest.fixture()
def sut(animator) -> StatusViewModel:
    return StatusViewModel(animator=animator)


class TestSetConfirmation:
    def test_invalidates_app(self, sut, app, get_app) -> None:
        with patch("prompt_toolkit.application.get_app", new=get_app):
            sut.set_confirmation(confirmation=Mock())

            app.invalidate.assert_called_once()


class TestStatusContent:
    def test_when_confirmation_none__no_alert_text__returns_empty_text(self, sut) -> None:
        expected = EMPTY_TEXT

        result = sut.status_content()

        assert result == expected

    def test_when_confirmation_not_none__returns_confirmation_ui_text(self, sut) -> None:
        expected = Mock()
        confirmation = create_autospec(Confirmation)
        confirmation.ui_text = expected

        sut.set_confirmation(confirmation)
        result = sut.status_content()

        assert result == expected

    def test_when_confirmation_none__returns_last_alert_text(self, sut) -> None:
        expected = Mock()

        sut.on_alert_text(expected)
        sut.set_confirmation(None)
        result = sut.status_content()

        assert result == expected


class TestStatusBackground:
    def test_when_confirmation_none__returns_bg0(self, sut) -> None:
        expected = Color.BG0

        sut.set_confirmation(None)
        result = sut.status_background()

        assert result == expected

    def test_when_confirmation_not_none__returns_red_dim(self, sut) -> None:
        expected = Color.RED_DIM

        sut.set_confirmation(Mock())
        result = sut.status_background()

        assert result == expected


class TestDidQueueAlert:
    def test_animates_alert_animation_with_on_alert_text_side_effect(
        self, sut, animator
    ) -> None:
        animation = Mock()
        alert = create_autospec(Alert)
        alert.animation = animation

        sut.did_queue_alert(alert)

        animator.animate.assert_called_once_with(
            animation=animation, side_effect=WeakMethod(sut.on_alert_text)
        )

    def test_when_confirmation_not_none__returns_red_dim(self, sut) -> None:
        expected = Color.RED_DIM

        sut.set_confirmation(Mock())
        result = sut.status_background()

        assert result == expected


class TestStatusView:
    @pytest.fixture()
    def viewmodel(self) -> StatusViewModel:
        return create_autospec(StatusViewModel)

    def test_text__returns_viewmodel_status_content(self, viewmodel) -> None:
        sut = StatusView(viewmodel=viewmodel)
        expected = viewmodel.status_content

        result = sut.text

        assert result == expected

    def test_background_color__returns_viewmodel_status_background(
        self, viewmodel
    ) -> None:
        sut = StatusView(viewmodel=viewmodel)
        expected = viewmodel.status_background

        result = sut.background_color

        assert result == expected
