from unittest.mock import Mock, create_autospec

import pytest
from marshmallow_generic import EXCLUDE, GenericSchema

from src.tuicub.common.http import BaseRequest, GameroomRequest
from src.tuicub.common.schemas import GameroomSchema


class MockBaseRequest(BaseRequest[Mock]):
    @property
    def path(self) -> str:
        return "foo"

    @property
    def response_schema(self) -> GenericSchema[Mock]:
        return self.mock_response_schema

    def __init__(self) -> None:
        self.mock_response_schema = create_autospec(GenericSchema)


@pytest.fixture()
def sut() -> MockBaseRequest:
    return MockBaseRequest()


class TestReturnsList:
    def test__returns_false(self, sut) -> None:
        expected = False

        result = sut.returns_list

        assert result == expected


class TestMapResponse:
    def test_deserializes_response_using_response_schema(self, sut) -> None:
        response = Mock()
        expected = Mock()
        sut.mock_response_schema.loads.return_value = expected

        result = sut.map_response(response=response)

        assert result == expected
        sut.mock_response_schema.loads.assert_called_once_with(
            json_data=response, many=False, unknown=EXCLUDE
        )


class MockGameroomRequest(GameroomRequest):
    @property
    def path(self) -> str:
        return "foo"


class TestGameroomRequest:
    def test_response_schema__returns_gameroom_schema(self, gameroom) -> None:
        sut = MockGameroomRequest(gameroom=gameroom)

        result = sut.response_schema

        assert isinstance(result, GameroomSchema)
