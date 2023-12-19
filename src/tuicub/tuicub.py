import asyncio
import tomllib

from prompt_toolkit.output.defaults import create_output
from pyllot import Router, ScreenPresenting

from .app.module import AppModule
from .common.config import Config
from .common.confirmation.module import ConfirmationModule
from .common.events.module import EventsModule
from .common.http.module import HttpModule
from .common.module import CommonModule
from .common.screens import ScreenName, ScreensFactory, TuicubScreen
from .common.services.module import ServicesModule
from .common.state import State
from .common.state.module import StateModule
from .common.transitions import (
    GAME_TO_GAMEROOMS,
    GAMEROOM_TO_GAME,
    GAMEROOM_TO_GAMEROOMS,
    GAMEROOMS_TO_GAMEROOM,
    REGISTER_USER_TO_GAMEROOMS,
)
from .common.views.color import Theme, is_colors_map
from .game.module import GameModule
from .gameroom.module import GameroomModule
from .gamerooms.module import GameroomsModule
from .register_user.module import RegisterUserModule


async def run(config: Config) -> int:
    stream_reader, stream_writer = await asyncio.open_connection(
        config.events_host, port=config.events_port
    )
    output = create_output()
    loop = asyncio.get_running_loop()
    theme = Theme.default()
    if config.theme_file:
        with config.theme_file.open("rb") as f:
            data = tomllib.load(f)
            if is_colors_map(data):
                theme = Theme(colors_map=data)

    common_module = CommonModule(config=config, theme=theme)
    state_module = StateModule(common_module=common_module)
    events_module = EventsModule(stream_reader=stream_reader, stream_writer=stream_writer)
    confirmation_module = ConfirmationModule(state_module=state_module, loop=loop)
    services_module = ServicesModule(
        confirmation_module=confirmation_module,
        events_module=events_module,
        state_module=state_module,
        output=output,
    )
    http_module = HttpModule(common_module=common_module, services_module=services_module)

    initial_screen = RegisterUserModule.assemble(
        state_module=state_module,
        services_module=services_module,
        events_module=events_module,
        common_module=common_module,
        http_module=http_module,
    )()
    app_module = AppModule(
        common_module=common_module,
        state_module=state_module,
        services_module=services_module,
        confirmation_module=confirmation_module,
        initial_screen=initial_screen,
        output=output,
    )

    screens_factory = ScreensFactory()
    screens_factory.add_factory(
        ScreenName.GAMEROOMS,
        GameroomsModule.assemble(
            state_module=state_module,
            services_module=services_module,
            common_module=common_module,
            http_module=http_module,
        ),
    )
    screens_factory.add_factory(
        ScreenName.GAMEROOM,
        GameroomModule.assemble(
            state_module=state_module,
            services_module=services_module,
            common_module=common_module,
            http_module=http_module,
            events_module=events_module,
        ),
    )
    screens_factory.add_factory(
        ScreenName.GAME,
        GameModule.assemble(
            state_module=state_module,
            services_module=services_module,
            common_module=common_module,
            http_module=http_module,
            events_module=events_module,
        ),
    )

    router: Router[State, TuicubScreen] = _create_router(
        initial_screen, presenter=app_module.view, screens_factory=screens_factory
    )

    state_module.store.subscribe(router)

    def pre_run() -> None:
        nonlocal initial_screen
        initial_screen.will_present()
        initial_screen.did_present()

    async with asyncio.TaskGroup() as group:
        group.create_task(events_module.socket_reader.start())
        group.create_task(app_module.app.run_async())

    return 0


def _create_router(
    initial_screen: TuicubScreen,
    presenter: ScreenPresenting[TuicubScreen],
    screens_factory: ScreensFactory,
) -> Router[State, TuicubScreen]:
    router: Router[State, TuicubScreen] = Router(
        initial_screen, presenter=presenter, screens_factory=screens_factory
    )
    router.add_transition(REGISTER_USER_TO_GAMEROOMS)
    router.add_transition(GAMEROOMS_TO_GAMEROOM)
    router.add_transition(GAMEROOM_TO_GAME)
    router.add_transition(GAME_TO_GAMEROOMS)
    router.add_transition(GAMEROOM_TO_GAMEROOMS)
    return router
