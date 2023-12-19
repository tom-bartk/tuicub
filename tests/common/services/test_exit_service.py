from unittest.mock import AsyncMock, create_autospec

import pytest
from asockit import SocketReader, SocketWriter

from src.tuicub.common.models import Keybind
from src.tuicub.common.services.exit_service import ExitService
from src.tuicub.common.strings import EXIT_KEYBIND_TOOLTIP


@pytest.fixture()
def socket_reader() -> SocketReader:
    return create_autospec(SocketReader)


@pytest.fixture()
def socket_writer() -> SocketWriter:
    return create_autospec(SocketWriter)


@pytest.fixture()
def sut(socket_reader, socket_writer, confirmation_service) -> ExitService:
    return ExitService(
        confirmation_service=confirmation_service,
        socket_reader=socket_reader,
        socket_writer=socket_writer,
    )


@pytest.mark.asyncio()
class TestExitApp:
    async def test_when_not_confirmed__does_not_exit_app(
        self, sut, event, confirmation_service
    ) -> None:
        confirmation_service.confirm = AsyncMock(return_value=False)

        await sut.exit_app(event)

        event.app.exit.assert_not_called()

    async def test_when_confirmed__exits_app(
        self, sut, event, confirmation_service
    ) -> None:
        confirmation_service.confirm = AsyncMock(return_value=True)

        await sut.exit_app(event)

        event.app.exit.assert_called_once()

    async def test_when_confirmed__stops_socket_reader(
        self, sut, event, confirmation_service, socket_reader
    ) -> None:
        confirmation_service.confirm = AsyncMock(return_value=True)

        await sut.exit_app(event)

        socket_reader.stop.assert_awaited_once()

    async def test_when_confirmed__closes_socket_writer(
        self, sut, event, confirmation_service, socket_writer
    ) -> None:
        confirmation_service.confirm = AsyncMock(return_value=True)

        await sut.exit_app(event)

        socket_writer.close.assert_awaited_once()


@pytest.mark.asyncio()
class TestForceExit:
    async def test_exits_app(self, sut, event) -> None:
        await sut.force_exit(event)

        event.app.exit.assert_called_once()

    async def test_stops_socket_reader(self, sut, event, socket_reader) -> None:
        await sut.force_exit(event)

        socket_reader.stop.assert_awaited_once()

    async def test_closes_socket_writer(self, sut, event, socket_writer) -> None:
        await sut.force_exit(event)

        socket_writer.close.assert_awaited_once()


class TestKeybind:
    def test_returns_q_keybind_with_exit_tooltip(self, sut) -> None:
        expected = Keybind(
            key="q", display_key="q", tooltip=EXIT_KEYBIND_TOOLTIP, action=sut.exit_app
        )

        result = sut.keybind

        assert result == expected
