from src.tuicub.register_user.module import RegisterUserModule
from src.tuicub.register_user.view import RegisterUserScreen


class TestAssemble:
    def test_returned_factory_creates_register_user_screen(
        self, state_module, services_module, events_module, common_module, http_module
    ) -> None:
        sut = RegisterUserModule.assemble(
            state_module=state_module,
            services_module=services_module,
            events_module=events_module,
            common_module=common_module,
            http_module=http_module,
        )

        result = sut()

        assert isinstance(result, RegisterUserScreen)
