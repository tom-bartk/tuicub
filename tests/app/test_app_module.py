import pytest
from prompt_toolkit.application import Application

from src.tuicub.app.module import AppModule
from src.tuicub.app.view import AppView


@pytest.fixture()
def sut(
    common_module,
    state_module,
    services_module,
    confirmation_module,
    initial_screen,
    output,
) -> AppModule:
    return AppModule(
        common_module=common_module,
        state_module=state_module,
        services_module=services_module,
        confirmation_module=confirmation_module,
        initial_screen=initial_screen,
        output=output,
    )


class TestAppModule:
    def test_app__returns_application_instance(self, sut) -> None:
        result = sut.app

        assert isinstance(result, Application)

    def test_view__returns_app_view_instance(self, sut) -> None:
        result = sut.view

        assert isinstance(result, AppView)
