import pytest

from src.tuicub.common.confirmation.service import ConfirmationService
from src.tuicub.common.services.alert_service import AlertService
from src.tuicub.common.services.auth_service import AuthService
from src.tuicub.common.services.exit_service import ExitService
from src.tuicub.common.services.module import ServicesModule
from src.tuicub.common.services.screen_size_service import ScreenSizeService


@pytest.fixture()
def sut(
    state_module,
    events_module,
    confirmation_module,
    output,
) -> ServicesModule:
    return ServicesModule(
        state_module=state_module,
        events_module=events_module,
        confirmation_module=confirmation_module,
        output=output,
    )


class TestServicesModule:
    def test_alert_service__returns_alert_service_instance(self, sut) -> None:
        result = sut.alert_service

        assert isinstance(result, AlertService)

    def test_auth_service__returns_auth_service_instance(self, sut) -> None:
        result = sut.auth_service

        assert isinstance(result, AuthService)

    def test_confirmation_service__returns_confirmation_service_instance(
        self, sut
    ) -> None:
        result = sut.confirmation_service

        assert isinstance(result, ConfirmationService)

    def test_exit_service__returns_exit_service_instance(self, sut) -> None:
        result = sut.exit_service

        assert isinstance(result, ExitService)

    def test_screen_size_service__returns_screen_size_service_instance(self, sut) -> None:
        result = sut.screen_size_service

        assert isinstance(result, ScreenSizeService)
