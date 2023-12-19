from src.tuicub.common.state import State
from src.tuicub.gameroom.module import GameroomModule
from src.tuicub.gameroom.view import GameroomScreen


class TestAssemble:
    def test_returned_factory_creates_gameroom_screen(
        self,
        state_module,
        services_module,
        common_module,
        http_module,
        events_module,
        gameroom,
    ) -> None:
        state_module.store.state = State(current_gameroom=gameroom)
        sut = GameroomModule.assemble(
            state_module=state_module,
            events_module=events_module,
            services_module=services_module,
            common_module=common_module,
            http_module=http_module,
        )

        result = sut()

        assert isinstance(result, GameroomScreen)
