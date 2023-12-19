import asyncio
from unittest.mock import AsyncMock, Mock, call, create_autospec

import pytest

from src.tuicub.app.actions import RemoveConfirmationAction, SetConfirmationAction
from src.tuicub.common.confirmation import ConfirmationFactory, ConfirmationService


@pytest.fixture()
def factory() -> ConfirmationFactory:
    return create_autospec(ConfirmationFactory)


@pytest.fixture()
def lock() -> asyncio.Lock:
    lock = Mock()
    lock.__aenter__ = AsyncMock()
    lock.__aexit__ = AsyncMock()
    return lock


@pytest.fixture()
def sut(factory, app_store, lock) -> ConfirmationService:
    return ConfirmationService(confirmation_factory=factory, store=app_store, lock=lock)


@pytest.mark.asyncio()
class TestConfirm:
    async def test_creates_confirmation_with_passed_text_using_factory(
        self, sut, factory
    ) -> None:
        expected = "foo"

        await sut.confirm(text="foo")

        factory.create.assert_called_once_with(text=expected)

    async def test_dispatches_set_confirmation_action_to_app_store(
        self, sut, factory, app_store
    ) -> None:
        confirmation = Mock()
        factory.create.return_value = confirmation
        expected = SetConfirmationAction(confirmation)

        await sut.confirm(text="foo")

        app_store.dispatch.assert_called_once_with(expected)

    async def test_dispatches_removes_confirmation_action_after_awaiting_result(
        self, sut, factory, app_store
    ) -> None:
        confirmation = Mock()
        confirmation.result = AsyncMock(return_value=True)
        factory.create.return_value = confirmation
        expected_calls = [
            call(SetConfirmationAction(confirmation)),
            call(RemoveConfirmationAction(result=True)),
        ]

        await sut.confirm(text="foo")

        app_store.dispatch.assert_has_calls(expected_calls)

    async def test_returns_result_of_awaiting_confirmation(self, sut, factory) -> None:
        confirmation = Mock()
        confirmation.result = AsyncMock(return_value=True)
        factory.create.return_value = confirmation
        expected = True

        result = await sut.confirm(text="foo")

        assert result == expected
