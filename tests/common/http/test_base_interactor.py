from typing import Any
from unittest.mock import AsyncMock, Mock, create_autospec

import pytest
from httperactor import Request

from src.tuicub.common.http import BaseHttpInteractor


class MockBaseHttpInteractor(BaseHttpInteractor[Mock]):
    def __init__(self, *args: Any, **kwargs: Any):
        self.mock_request = create_autospec(Request)
        super().__init__(*args, **kwargs)

    @property
    def request(self) -> Request[Mock]:
        return self.mock_request


class MockConfirmingBaseHttpInteractor(MockBaseHttpInteractor):
    @property
    def confirmation(self) -> str:
        return "foo"


@pytest.fixture()
def sut(
    auth_middleware, confirmation_service, http_client, store
) -> MockBaseHttpInteractor:
    return MockBaseHttpInteractor(
        auth=auth_middleware,
        confirmation_service=confirmation_service,
        http_client=http_client,
        store=store,
    )


@pytest.fixture()
def confirming_sut(
    auth_middleware, confirmation_service, http_client, store
) -> MockConfirmingBaseHttpInteractor:
    return MockConfirmingBaseHttpInteractor(
        auth=auth_middleware,
        confirmation_service=confirmation_service,
        http_client=http_client,
        store=store,
    )


class TestAuth:
    def test_returns_auth_middleware(self, sut, auth_middleware) -> None:
        expected = auth_middleware

        result = sut.auth

        assert result == expected


class TestConfirmation:
    def test_returns_empty_string(self, sut) -> None:
        expected = ""

        result = sut.confirmation

        assert result == expected


class TestExecute:
    @pytest.mark.asyncio()
    async def test_by_default_does_not_ask_for_confirmation(
        self, sut, confirmation_service
    ) -> None:
        await sut.execute()

        confirmation_service.confirm.assert_not_awaited()

    @pytest.mark.asyncio()
    async def test_when_has_confirmation__answer_false__does_not_perform_request(
        self, confirming_sut, confirmation_service, http_client
    ) -> None:
        confirmation_service.confirm = AsyncMock(return_value=False)

        await confirming_sut.execute()

        http_client.send.assert_not_awaited()

    @pytest.mark.asyncio()
    async def test_when_has_confirmation__answer_true__performs_request(
        self, confirming_sut, confirmation_service, http_client
    ) -> None:
        confirmation_service.confirm = AsyncMock(return_value=True)

        await confirming_sut.execute()

        http_client.send.assert_awaited_with(
            confirming_sut.request, auth=confirming_sut.auth
        )
