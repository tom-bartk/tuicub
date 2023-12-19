from src.tuicub.gamerooms.module import GameroomsModule
from src.tuicub.gamerooms.view import GameroomsScreen


class TestAssemble:
    def test_returned_factory_creates_gamerooms_screen(
        self, state_module, services_module, common_module, http_module
    ) -> None:
        sut = GameroomsModule.assemble(
            state_module=state_module,
            services_module=services_module,
            common_module=common_module,
            http_module=http_module,
        )

        result = sut()

        assert isinstance(result, GameroomsScreen)
