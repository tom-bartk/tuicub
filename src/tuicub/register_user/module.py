from collections.abc import Callable

from ..common.events.module import EventsModule
from ..common.http.module import HttpModule
from ..common.module import CommonModule
from ..common.services.module import ServicesModule
from ..common.state.module import StateModule
from ..common.state.store import TuicubStore
from .controller import RegisterUserController
from .keybinds import RegisterUserKeybindsContainer
from .request import RegisterUserInteractor
from .state import RegisterUserState, SetNameReducer
from .view import RegisterUserContent, RegisterUserScreen, RegisterUserView


class RegisterUserModule:
    @classmethod
    def assemble(
        cls,
        state_module: StateModule,
        services_module: ServicesModule,
        events_module: EventsModule,
        common_module: CommonModule,
        http_module: HttpModule,
    ) -> Callable[[], RegisterUserScreen]:
        def factory() -> RegisterUserScreen:
            local_store = TuicubStore(
                initial_state=RegisterUserState(), logger=common_module.logger
            )
            local_store.register(SetNameReducer())

            controller = RegisterUserController(
                store=state_module.store,
                local_store=local_store,
                register_user_interactor=RegisterUserInteractor(
                    auth_service=services_module.auth_service,
                    socket_writer=events_module.socket_writer,
                    auth=http_module.auth_middleware,
                    http_client=http_module.client,
                    store=state_module.store,
                    local_store=local_store,
                    confirmation_service=services_module.confirmation_service,
                ),
            )

            content = RegisterUserContent(theme=common_module.theme)
            content.textfield.set_delegate(controller)

            keybinds_container = RegisterUserKeybindsContainer(
                controller=controller, app_store=state_module.app_store
            )
            view = RegisterUserView(
                content=content, keybinds_container=keybinds_container
            )

            return RegisterUserScreen(view=view, keybinds_container=keybinds_container)

        return factory
