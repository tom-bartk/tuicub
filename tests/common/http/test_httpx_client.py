from unittest.mock import create_autospec

import httpx
import pytest

from src.tuicub.common.http import TuicubHttpxClient


@pytest.fixture()
def sut(config, logger) -> TuicubHttpxClient:
    return TuicubHttpxClient(config=config, logger=logger)


class TestLogRequest:
    @pytest.mark.asyncio()
    async def test_logs_http_request_using_logger(self, sut, logger) -> None:
        request = create_autospec(httpx.Request)

        await sut.log_request(request)

        logger.log_http_request.assert_called_once_with(request)


class TestLogResponse:
    @pytest.mark.asyncio()
    async def test_logs_http_response_using_logger(self, sut, logger) -> None:
        response = create_autospec(httpx.Response)

        await sut.log_response(response)

        logger.log_http_response.assert_called_once_with(response)


class TestEventHooks:
    def test_returns_dict_with__request_as_log_request__response_as_log_response(
        self, sut
    ) -> None:
        expected = {
            "request": [sut.log_request],
            "response": [sut.log_response],
        }

        result = sut.event_hooks

        assert result == expected
