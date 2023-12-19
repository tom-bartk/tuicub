import pytest

from src.tuicub.common.state.module import StateModule
from src.tuicub.common.state.store import TuicubStore


@pytest.fixture()
def sut(common_module) -> StateModule:
    return StateModule(common_module=common_module)


class TestStateModule:
    def test_app_store__returns_tuicub_store_instance(self, sut) -> None:
        result = sut.app_store

        assert isinstance(result, TuicubStore)

    def test_store__returns_tuicub_store_instance(self, sut) -> None:
        result = sut.store

        assert isinstance(result, TuicubStore)
