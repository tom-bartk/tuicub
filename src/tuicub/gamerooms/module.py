from collections.abc import Callable

from ..common.http.module import HttpModule
from ..common.module import CommonModule
from ..common.services.module import ServicesModule
from ..common.state.module import StateModule
from ..common.state.store import TuicubStore
from .controller import GameroomsController
from .keybinds import GameroomsKeybindsContainer
from .requests import (
    CreateGameroomInteractor,
    GetGameroomsInteractor,
    JoinGameroomInteractor,
)
from .state import GameroomsState, ScrollGameroomsReducer, SetGameroomsRowsReducer
from .view import GameroomsListView, GameroomsScreen, GameroomsView
from .viewmodel import GameroomsViewModel


class GameroomsModule:
    @classmethod
    def assemble(
        cls,
        state_module: StateModule,
        services_module: ServicesModule,
        common_module: CommonModule,
        http_module: HttpModule,
    ) -> Callable[[], GameroomsScreen]:
        def factory() -> GameroomsScreen:
            local_store = TuicubStore(
                initial_state=GameroomsState(), logger=common_module.logger
            )
            local_store.register(ScrollGameroomsReducer())
            local_store.register(SetGameroomsRowsReducer())

            controller = GameroomsController(
                store=state_module.store,
                local_store=local_store,
                get_gamerooms_interactor=GetGameroomsInteractor(
                    auth=http_module.auth_middleware,
                    confirmation_service=services_module.confirmation_service,
                    http_client=http_module.client,
                    store=state_module.store,
                ),
                join_gameroom_interactor=JoinGameroomInteractor(
                    auth=http_module.auth_middleware,
                    confirmation_service=services_module.confirmation_service,
                    http_client=http_module.client,
                    store=state_module.store,
                    local_store=local_store,
                ),
                create_gameroom_interactor=CreateGameroomInteractor(
                    auth=http_module.auth_middleware,
                    confirmation_service=services_module.confirmation_service,
                    http_client=http_module.client,
                    store=state_module.store,
                ),
            )
            keybinds_container = GameroomsKeybindsContainer(
                controller=controller, app_store=state_module.app_store
            )

            viewmodel = GameroomsViewModel(
                store=state_module.store, local_store=local_store
            )
            list_view = GameroomsListView(
                viewmodel=viewmodel,
                cache=common_module.cache(),
                theme=common_module.theme,
            )
            view = GameroomsView(
                viewmodel=viewmodel,
                list_view=list_view,
                keybinds_container=keybinds_container,
            )
            screen = GameroomsScreen(view=view, keybinds_container=keybinds_container)
            screen.set_delegate(delegate=controller)
            return screen

        return factory
