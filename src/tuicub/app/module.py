from prompt_toolkit.application import Application
from prompt_toolkit.filters import buffer_has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.output import Output
from prompt_toolkit.renderer import ColorDepth

from ..common.confirmation.module import ConfirmationModule
from ..common.module import CommonModule
from ..common.screens import TuicubScreen
from ..common.services.module import ServicesModule
from ..common.state.module import StateModule
from ..common.views.animation import TextAnimator
from .controller import AppController
from .status import StatusView, StatusViewModel
from .view import AppView
from .viewmodel import AppViewModel


class AppModule:
    __slots__ = ("_app", "_view")

    @property
    def app(self) -> Application:
        return self._app

    @property
    def view(self) -> AppView:
        return self._view

    def __init__(
        self,
        common_module: CommonModule,
        state_module: StateModule,
        services_module: ServicesModule,
        confirmation_module: ConfirmationModule,
        initial_screen: TuicubScreen,
        output: Output,
    ):
        status_viewmodel = StatusViewModel(animator=TextAnimator())
        services_module.alert_service.set_delegate(status_viewmodel)

        controller = AppController(confirm_interactor=confirmation_module.interactor)

        bindings = KeyBindings()
        bindings.add("y", filter=~buffer_has_focus)(controller.answer_confirmation_yes)
        bindings.add("n", filter=~buffer_has_focus)(controller.answer_confirmation_no)
        bindings.add("escape", filter=~buffer_has_focus)(
            controller.answer_confirmation_no
        )
        bindings.add("q", filter=~buffer_has_focus)(services_module.exit_service.exit_app)
        bindings.add("c-c")(services_module.exit_service.force_exit)

        self._view: AppView = AppView(
            initial_screen=initial_screen,
            status_view=StatusView(viewmodel=status_viewmodel, theme=common_module.theme),
            viewmodel=AppViewModel(
                local_store=state_module.app_store,
                global_keybinds=[services_module.exit_service.keybind],
                status_viewmodel=status_viewmodel,
            ),
            theme=common_module.theme,
        )

        self._app: Application = Application(
            layout=Layout(self._view),
            key_bindings=bindings,
            full_screen=True,
            color_depth=ColorDepth.TRUE_COLOR,
            output=output,
        )
