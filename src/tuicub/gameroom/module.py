from collections.abc import Callable

from eventoolkit import EventsObserver

from ..common.events.module import EventsModule
from ..common.http.module import HttpModule
from ..common.module import CommonModule
from ..common.services.module import ServicesModule
from ..common.state.module import StateModule
from .controller import GameroomController
from .events import (
    GameroomDeletedEventHandler,
    GameStartedEventHandler,
    UserJoinedEventHandler,
    UserLeftEventHandler,
)
from .keybinds import GameroomKeybindsContainer
from .requests import (
    DeleteGameroomInteractor,
    LeaveGameroomInteractor,
    StartGameInteractor,
)
from .view import GameroomPlayersListView, GameroomScreen, GameroomView
from .viewmodel import GameroomViewModel


class GameroomModule:
    @classmethod
    def assemble(
        cls,
        state_module: StateModule,
        services_module: ServicesModule,
        common_module: CommonModule,
        http_module: HttpModule,
        events_module: EventsModule,
    ) -> Callable[[], GameroomScreen]:
        def factory() -> GameroomScreen:
            controller = GameroomController(
                store=state_module.store,
                leave_gameroom_interactor=LeaveGameroomInteractor(
                    auth=http_module.auth_middleware,
                    confirmation_service=services_module.confirmation_service,
                    http_client=http_module.client,
                    store=state_module.store,
                ),
                delete_gameroom_interactor=DeleteGameroomInteractor(
                    auth=http_module.auth_middleware,
                    confirmation_service=services_module.confirmation_service,
                    http_client=http_module.client,
                    store=state_module.store,
                ),
                start_game_interactor=StartGameInteractor(
                    auth=http_module.auth_middleware,
                    confirmation_service=services_module.confirmation_service,
                    http_client=http_module.client,
                    store=state_module.store,
                ),
            )

            events_observer = EventsObserver(
                GameroomDeletedEventHandler(
                    alert_service=services_module.alert_service, store=state_module.store
                ),
                GameStartedEventHandler(
                    alert_service=services_module.alert_service, store=state_module.store
                ),
                UserJoinedEventHandler(
                    alert_service=services_module.alert_service, store=state_module.store
                ),
                UserLeftEventHandler(
                    alert_service=services_module.alert_service, store=state_module.store
                ),
                publisher=events_module.publisher,
            )
            viewmodel = GameroomViewModel(
                store=state_module.store, events_observer=events_observer
            )

            keybinds_container = GameroomKeybindsContainer(
                controller=controller,
                store=state_module.store,
                app_store=state_module.app_store,
            )
            list_view = GameroomPlayersListView(
                viewmodel=viewmodel,
                cache=common_module.cache(),
                theme=common_module.theme,
            )
            view = GameroomView(
                viewmodel=viewmodel,
                list_view=list_view,
                keybinds_container=keybinds_container,
            )
            return GameroomScreen(view=view, keybinds_container=keybinds_container)

        return factory
