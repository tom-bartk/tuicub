from abc import abstractmethod
from typing import Generic, TypeVar

from httperactor import Request
from marshmallow_generic import EXCLUDE, GenericSchema

from ..models import Gameroom
from ..schemas import GameroomSchema

TResponse = TypeVar("TResponse")


class BaseRequest(Generic[TResponse], Request[TResponse]):
    """Base class for an http request."""

    __slots__ = ()

    @property
    def returns_list(self) -> bool:
        return False

    @property
    @abstractmethod
    def response_schema(self) -> GenericSchema[TResponse]:
        """The schema of the response."""

    def map_response(self, response: str) -> TResponse:
        """Map the raw response into an object instance.

        Args:
            response (str): The raw text response.

        Returns:
            The mapped response object.
        """
        return self.response_schema.loads(  # type: ignore
            json_data=response, many=self.returns_list, unknown=EXCLUDE
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseRequest):
            return NotImplemented
        return (
            self.path == other.path
            and self.method == other.method
            and self.body == other.body
            and self.headers == other.headers
            and self.returns_list == other.returns_list
        )


class GameroomRequest(BaseRequest[Gameroom]):
    """Base class for a gameroom http request."""

    __slots__ = ("_gameroom",)

    @property
    def response_schema(self) -> GenericSchema[Gameroom]:
        return GameroomSchema()

    def __init__(self, gameroom: Gameroom):
        self._gameroom: Gameroom = gameroom
