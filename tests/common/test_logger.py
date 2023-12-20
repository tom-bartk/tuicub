from collections.abc import Callable
from io import TextIOWrapper
from pathlib import Path
from unittest.mock import Mock, create_autospec, patch

import httpx
import pytest
import structlog
from attrs import frozen
from pydepot import Action

from src.tuicub.common.logger import Logger


@pytest.fixture()
def logfile_path() -> Path:
    return create_autospec(Path)


@pytest.fixture()
def create_sut(logfile_path) -> Callable[[bool], Logger]:
    def factory(debug: bool = True) -> Logger:
        return Logger(logfile_path=logfile_path, debug=debug)

    return factory


@pytest.fixture()
def mock_open() -> Mock:
    context_manager = Mock()
    context_manager.__enter__ = Mock()
    context_manager.__exit__ = Mock()
    return context_manager


@pytest.fixture()
def mock_log() -> structlog.types.FilteringBoundLogger:
    return create_autospec(structlog.types.FilteringBoundLogger)


class TestConfigure:
    def test_opens_logfile_for_appending(self, create_sut, logfile_path) -> None:
        sut = create_sut()

        with patch("builtins.open") as mocked_open:
            sut.configure()

            mocked_open.assert_called_with(logfile_path, "a")

    def test_registers_close_logfile_atexit_callback(self, create_sut) -> None:
        sut = create_sut()
        logfile = create_autospec(TextIOWrapper)

        with patch("builtins.open", return_value=logfile), patch(
            "atexit.register"
        ) as mocked_register:
            sut.configure()

            mocked_register.assert_called_with(logfile.close)

    def test_configures_structlog(self, create_sut) -> None:
        sut = create_sut()

        with patch("builtins.open"), patch("structlog.configure") as mocked_configure:
            sut.configure()

            mocked_configure.assert_called_once()


class TestLogHttpRequest:
    def test_when_debug__logs_info_with_method_and_path(
        self, create_sut, mock_log
    ) -> None:
        request = create_autospec(httpx.Request)
        request.method = "POST"
        request.url = Mock()
        request.url.path = "/foo"
        sut = create_sut()

        with patch("structlog.get_logger", return_value=mock_log):
            sut.log_http_request(request)

            mock_log.info.assert_called_once_with(
                "http_request", method="POST", path="/foo"
            )

    def test_when_not_debug__does_not_log(self, create_sut, mock_log) -> None:
        request = create_autospec(httpx.Request)
        request.url = Mock()
        request.method = "POST"
        request.url.path = "/foo"
        sut = create_sut(debug=False)

        with patch("structlog.get_logger", return_value=mock_log):
            sut.log_http_request(request)

            mock_log.info.assert_not_called()


class TestLogHttpResponse:
    def test_when_debug__logs_info_with_method_path_and_code(
        self, create_sut, mock_log
    ) -> None:
        request = create_autospec(httpx.Request)
        request.url = Mock()
        request.method = "POST"
        request.url.path = "/foo"

        response = create_autospec(httpx.Response)
        response.request = request
        response.status_code = 200
        sut = create_sut()

        with patch("structlog.get_logger", return_value=mock_log):
            sut.log_http_response(response)

            mock_log.info.assert_called_once_with(
                "http_response", method="POST", path="/foo", code=200
            )

    def test_when_not_debug__does_not_log(self, create_sut, mock_log) -> None:
        request = create_autospec(httpx.Request)
        request.url = Mock()
        request.method = "POST"
        request.url.path = "/foo"

        response = create_autospec(httpx.Response)
        response.request = request
        response.status_code = 200
        sut = create_sut(debug=False)

        with patch("structlog.get_logger", return_value=mock_log):
            sut.log_http_response(response)

            mock_log.info.assert_not_called()


@frozen
class MockAction(Action):
    foo: int


class TestLogAction:
    def test_when_debug__logs_info_with_action_name_and_params(
        self, create_sut, mock_log
    ) -> None:
        action = MockAction(foo=42)
        sut = create_sut()

        with patch("structlog.get_logger", return_value=mock_log):
            sut.log_action(action)

            mock_log.info.assert_called_once_with(
                "action_dispatch", action_name="MockAction", foo=42
            )

    def test_when_not_debug__does_not_log(self, create_sut, mock_log) -> None:
        action = MockAction(foo=42)
        sut = create_sut(debug=False)

        with patch("structlog.get_logger", return_value=mock_log):
            sut.log_action(action)

            mock_log.info.assert_not_called()
