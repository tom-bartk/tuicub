import asyncio
from unittest.mock import AsyncMock, Mock, create_autospec, patch

from src.tuicub.app.state import AppState
from src.tuicub.common.models import Keybind
from src.tuicub.common.utils import async_run, create_filter


class TestAsyncRun:
    def test_adds_done_callback_to_task(self, loop) -> None:
        coro = AsyncMock()
        task = create_autospec(asyncio.Task)
        loop.create_task.return_value = task

        with patch("asyncio.get_running_loop", return_value=loop):
            async_run(coro)

            task.add_done_callback.assert_called_once()

    def test_creates_task_with_coroutine_using_current_loop(self, loop) -> None:
        coro = AsyncMock()
        with patch("asyncio.get_running_loop", return_value=loop):
            async_run(coro)

            loop.create_task.assert_called_once_with(coro)


class TestCreateFilter:
    def test_when_has_confirmation__filter_false(self, app_store) -> None:
        app_store.state = AppState(confirmation=Mock())
        keybind = create_autospec(Keybind)
        keybind.pt_filter = Mock(return_value=True)
        keybind.condition = Mock(return_value=True)
        expected = False

        _filter = create_filter(app_store=app_store, keybind=keybind)
        result = _filter()

        assert result == expected

    def test_when_has_no_confirmation__keybind_pt_filter_false__filter_false(
        self, app_store
    ) -> None:
        app_store.state = AppState(confirmation=None)
        keybind = create_autospec(Keybind)
        keybind.pt_filter = Mock(return_value=False)
        keybind.condition = Mock(return_value=True)
        expected = False

        _filter = create_filter(app_store=app_store, keybind=keybind)
        result = _filter()

        assert result == expected

    def test_when_has_no_confirmation__keybind_condition_false__filter_false(
        self, app_store
    ) -> None:
        app_store.state = AppState(confirmation=None)
        keybind = create_autospec(Keybind)
        keybind.pt_filter = Mock(return_value=True)
        keybind.condition = Mock(return_value=False)
        expected = False

        _filter = create_filter(app_store=app_store, keybind=keybind)
        result = _filter()

        assert result == expected

    def test_when_has_no_confirmation__keybind_condition_and_pt_filter_true__filter_true(
        self, app_store
    ) -> None:
        app_store.state = AppState(confirmation=None)
        keybind = create_autospec(Keybind)
        keybind.pt_filter = Mock(return_value=True)
        keybind.condition = Mock(return_value=True)
        expected = True

        _filter = create_filter(app_store=app_store, keybind=keybind)
        result = _filter()

        assert result == expected
