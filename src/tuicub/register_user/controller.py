from prompt_toolkit.key_binding import KeyPressEvent
from pydepot import Store

from ..common import utils
from ..common.state import State
from .request import RegisterUserInteractor
from .state import RegisterUserState, SetNameAction


class RegisterUserController:
    """Captures and converts user input to interactions in the register user screen."""

    __slots__ = ("_store", "_local_store", "_register_user_interactor", "__weakref__")

    def __init__(
        self,
        store: Store[State],
        local_store: Store[RegisterUserState],
        register_user_interactor: RegisterUserInteractor,
    ):
        """Initialize new controller.

        Args:
            store (Store[State]): The global store.
            local_store (Store[RegisterUserState]): The local screen store.
            register_user_interactor (RegisterUserInteractor): The interactor for
                the register user request.
        """
        self._store: Store[State] = store
        self._local_store: Store[RegisterUserState] = local_store
        self._register_user_interactor: RegisterUserInteractor = register_user_interactor

    def on_text_changed(self, text: str) -> None:
        """Callback of the `TextfieldViewDelegate`.

        Called whenever the text value of a textfield changes.
        Dispatches a `SetNameAction` to the local store with the updated text as the name.

        Args:
            text (str): The updated text of the textfield.
        """
        self._local_store.dispatch(SetNameAction(name=text))

    def register_user(self, event: KeyPressEvent) -> None:
        """Handler for the submit keybind.

        Sends the register user request.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        utils.async_run(self._register_user_interactor.execute())
