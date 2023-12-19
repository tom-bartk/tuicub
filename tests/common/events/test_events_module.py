import asyncio
from unittest.mock import create_autospec

import asockit
import pytest
from eventoolkit import EventPublisher

from src.tuicub.common.events.module import EventsModule


@pytest.fixture()
def stream_reader() -> asyncio.StreamReader:
    return create_autospec(asyncio.StreamReader)


@pytest.fixture()
def stream_writer() -> asyncio.StreamWriter:
    return create_autospec(asyncio.StreamWriter)


@pytest.fixture()
def sut(stream_reader, stream_writer) -> EventsModule:
    return EventsModule(stream_reader=stream_reader, stream_writer=stream_writer)


class TestEventsModule:
    def test_publisher__returns_event_publisher_instance(self, sut) -> None:
        result = sut.publisher

        assert isinstance(result, EventPublisher)

    def test_socket_reader__returns_socket_reader_instance(self, sut) -> None:
        result = sut.socket_reader

        assert isinstance(result, asockit.SocketReader)

    def test_socket_writer__returns_socket_writer_instance(self, sut) -> None:
        result = sut.socket_writer

        assert isinstance(result, asockit.SocketWriter)
