import pytest
from attrs import field, frozen
from pydepot import Action

from src.tuicub.common.state.store import TuicubStore


@frozen
class MockState:
    foo: int = field(default=42)


@frozen
class MockAction(Action):
    foo: int


@pytest.fixture()
def sut(logger) -> TuicubStore[MockState]:
    return TuicubStore(initial_state=MockState(), logger=logger)


class TestDispatch:
    def test_logs_action_with_logger(self, sut, logger) -> None:
        sut.dispatch(MockAction(foo=13))

        logger.log_action.assert_called_once_with(MockAction(foo=13))
