from unittest.mock import Mock, patch

import pytest

from src.tuicub.common.state import State
from src.tuicub.common.views import Text
from src.tuicub.gameroom.view import UserRowViewModel
from src.tuicub.gameroom.viewmodel import GameroomViewModel


@pytest.fixture()
def sut(store, events_observer) -> GameroomViewModel:
    return GameroomViewModel(store=store, events_observer=events_observer)


class TestRows:
    def test_when_no_global_state_changes__returns_empty_typle(self, sut) -> None:
        expected = ()

        result = sut.rows()

        assert result == expected

    def test_when_global_state_changed_w_current_gameroom__returns_user_rows(
        self, sut, user_1, user_2, user_3, gameroom
    ) -> None:
        expected = (
            UserRowViewModel(user=user_1, is_owner=True),
            UserRowViewModel(user=user_2, is_owner=False),
            UserRowViewModel(user=user_3, is_owner=False),
        )

        sut.on_state(State(current_gameroom=gameroom))
        result = sut.rows()

        assert result == expected

    def test_when_global_state_changed_w_none_current_gameroom__returns_empty_tuple(
        self, sut
    ) -> None:
        expected = ()

        sut.on_state(State(current_gameroom=None))
        result = sut.rows()

        assert result == expected

    def test_gameroom_text__when_state_has_current_gameroom__returns_gameroom_text(
        self, sut, store, gameroom
    ) -> None:
        store.state = State(current_gameroom=gameroom)
        expected = Mock()

        with patch(
            "src.tuicub.common.views.gameroom.gameroom_text", return_value=expected
        ):
            result = sut.gameroom_text()

            assert result == expected

    def test_gameroom_text__when_state_has_no_current_gameroom__returns_empty_text(
        self, sut, store
    ) -> None:
        store.state = State(current_gameroom=None)
        expected = Text()

        with patch("src.tuicub.common.views.gameroom.gameroom_text"):
            result = sut.gameroom_text()

            assert result == expected

    def test_gameroom_text__when_state_has_current_gameroom__calls_gameroom_text_with_it(
        self, sut, store, gameroom
    ) -> None:
        store.state = State(current_gameroom=gameroom)

        with patch(
            "src.tuicub.common.views.gameroom.gameroom_text"
        ) as mocked_gameroom_text:
            _ = sut.gameroom_text()

            mocked_gameroom_text.assert_called_once_with(
                gameroom=gameroom, is_highlighted=False, horizontal_padding=0
            )


class TestOnGlobalState:
    def test_invalidates_app(self, sut, get_app, app) -> None:
        with patch("prompt_toolkit.application.get_app", new=get_app):
            sut.on_state(State())

            app.invalidate.assert_called_once()


class TestSubscribe:
    def test_subscribes_to_store_and_starts_events_observer(
        self, sut, store, events_observer
    ) -> None:
        sut.subscribe()

        store.subscribe.assert_called_once_with(sut, include_current=True)
        events_observer.observe.assert_called_once()


class TestUnsubscribe:
    def test_unsubscribes_from_store_and_stops_events_observer(
        self, sut, store, events_observer
    ) -> None:
        sut.unsubscribe()

        store.unsubscribe.assert_called_once_with(sut)
        events_observer.stop.assert_called_once()
