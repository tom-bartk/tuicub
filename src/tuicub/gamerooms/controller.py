from prompt_toolkit.key_binding import KeyPressEvent
from pydepot import Store

from ..common import utils
from ..common.screens import TuicubScreen
from ..common.state import State
from ..common.views import ScrollDirection
from .requests import (
    CreateGameroomInteractor,
    GetGameroomsInteractor,
    JoinGameroomInteractor,
)
from .state import GameroomsState, ScrollGameroomsAction


class GameroomsController:
    """Captures and converts user input to interactions in the gamerooms screen."""

    __slots__ = (
        "_store",
        "_local_store",
        "_get_gamerooms_interactor",
        "_join_gameroom_interactor",
        "_create_gameroom_interactor",
        "__weakref__",
    )

    def __init__(
        self,
        store: Store[State],
        local_store: Store[GameroomsState],
        get_gamerooms_interactor: GetGameroomsInteractor,
        join_gameroom_interactor: JoinGameroomInteractor,
        create_gameroom_interactor: CreateGameroomInteractor,
    ):
        """Initialize new controller.

        Args:
            store (Store[State]): The global store.
            local_store (Store[GameroomsState]): The local screen store.
            get_gamerooms_interactor (GetGameroomsInteractor): The interactor for
                the get gamerooms request.
            join_gameroom_interactor (JoinGameroomInteractor): The interactor for
                the join gameroom request.
            create_gameroom_interactor (CreateGameroomInteractor): The interactor for
                the create gameroom request.
        """
        self._store: Store[State] = store
        self._local_store: Store[GameroomsState] = local_store
        self._get_gamerooms_interactor: GetGameroomsInteractor = get_gamerooms_interactor
        self._join_gameroom_interactor: JoinGameroomInteractor = join_gameroom_interactor
        self._create_gameroom_interactor: CreateGameroomInteractor = (
            create_gameroom_interactor
        )

    def screen_did_present(self, screen: TuicubScreen) -> None:
        """Callback of the `ScreenLifecycleDelegate`.

        Called whenever the screen is presented. Sends a get gamerooms request.

        Args:
            screen (TuicubScreen): The presented screen.
        """
        utils.async_run(self._get_gamerooms_interactor.execute())

    def refresh_gamerooms(self, event: KeyPressEvent) -> None:
        """Handler for the refresh keybind.

        Sends a get gamerooms request.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        utils.async_run(self._get_gamerooms_interactor.execute())

    def scroll_gamerooms_down(self, event: KeyPressEvent) -> None:
        """Handler for the scroll down keybind.

        Dispatches a `ScrollGameroomsAction` to the local store with the down direction.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._local_store.dispatch(ScrollGameroomsAction(ScrollDirection.DOWN))

    def scroll_gamerooms_up(self, event: KeyPressEvent) -> None:
        """Handler for the scroll up keybind.

        Dispatches a `ScrollGameroomsAction` to the local store with the up direction.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._local_store.dispatch(ScrollGameroomsAction(ScrollDirection.UP))

    def join_gameroom(self, event: KeyPressEvent) -> None:
        """Handler for the join keybind.

        Sends a join gameroom request if the global store has at least one gameroom.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        if self._store.state.gamerooms:
            utils.async_run(self._join_gameroom_interactor.execute())

    def create_gameroom(self, event: KeyPressEvent) -> None:
        """Handler for the create gameroom keybind.

        Sends a create gameroom request.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        utils.async_run(self._create_gameroom_interactor.execute())
