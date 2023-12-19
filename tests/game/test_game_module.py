import pytest

from src.tuicub.common.state import State
from src.tuicub.game.errors import NoCurrentGameError, NoCurrentUserError
from src.tuicub.game.module import GameModule
from src.tuicub.game.view import GameScreen


class TestAssemble:
    def test_returned_factory_creates_game_screen(
        self,
        state_module,
        services_module,
        common_module,
        http_module,
        events_module,
        game,
        user_1,
    ) -> None:
        state_module.store.state = State(current_user=user_1, current_game=game)
        sut = GameModule.assemble(
            state_module=state_module,
            events_module=events_module,
            services_module=services_module,
            common_module=common_module,
            http_module=http_module,
        )

        result = sut()

        assert isinstance(result, GameScreen)

    def test_when_no_current_user__raises_no_current_user_error(
        self,
        state_module,
        services_module,
        common_module,
        http_module,
        events_module,
        game,
    ) -> None:
        state_module.store.state = State(current_user=None, current_game=game)
        sut = GameModule.assemble(
            state_module=state_module,
            events_module=events_module,
            services_module=services_module,
            common_module=common_module,
            http_module=http_module,
        )

        with pytest.raises(NoCurrentUserError):
            sut()

    def test_when_no_current_game__raises_no_current_game_error(
        self,
        state_module,
        services_module,
        common_module,
        http_module,
        events_module,
        user_1,
    ) -> None:
        state_module.store.state = State(current_user=user_1, current_game=None)
        sut = GameModule.assemble(
            state_module=state_module,
            events_module=events_module,
            services_module=services_module,
            common_module=common_module,
            http_module=http_module,
        )

        with pytest.raises(NoCurrentGameError):
            sut()
