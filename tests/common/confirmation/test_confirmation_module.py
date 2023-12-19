import pytest

from src.tuicub.common.confirmation.factory import FutureConfirmationFactory
from src.tuicub.common.confirmation.interactor import ConfirmInteractor
from src.tuicub.common.confirmation.module import ConfirmationModule


@pytest.fixture()
def sut(state_module, loop) -> ConfirmationModule:
    return ConfirmationModule(state_module=state_module, loop=loop)


class TestConfirmationModule:
    def test_factory__returns_future_confirmation_factory_instance(self, sut) -> None:
        result = sut.factory

        assert isinstance(result, FutureConfirmationFactory)

    def test_interactor__returns_confirm_interactor_instance(self, sut) -> None:
        result = sut.interactor

        assert isinstance(result, ConfirmInteractor)
