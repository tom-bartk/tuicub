from attrs import evolve, field, frozen
from pydepot import Action, Reducer

from ..common.models import Gameroom
from ..common.views import ScrollDirection
from .view import GameroomRowViewModel


@frozen
class GameroomsState:
    """The local state of the gamerooms screen.

    Attributes:
        rows (tuple[GameroomRowViewModel, ...]): The current rows of the gamerooms list.
        selected_index (int): The index of the currently highlighted row.
    """

    rows: tuple[GameroomRowViewModel, ...] = field(default=())
    selected_index: int = field(default=0)


@frozen
class ScrollGameroomsAction(Action):
    """An intent to scroll the gamerooms list.

    Attributes:
        direction (ScrollDirection): The direction of the scroll.
    """

    direction: ScrollDirection


@frozen
class SetGameroomsRowsAction(Action):
    """An intent to update rows of the gamerooms list.

    Attributes:
        gamerooms (tuple[Gameroom, ...]): The gamerooms to create rows for.
    """

    gamerooms: tuple[Gameroom, ...]


class SetGameroomsRowsReducer(Reducer[SetGameroomsRowsAction, GameroomsState]):
    """The reducer for the set gamerooms rows action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetGameroomsRowsAction]:
        return SetGameroomsRowsAction

    def apply(
        self, action: SetGameroomsRowsAction, state: GameroomsState
    ) -> GameroomsState:
        """Apply the set gamerooms rows action.

        Creates a list of gamerooms rows while preserving the highlighted row index.

        Args:
            action (SetGameroomsRowsAction): The action to apply.
            state (GameroomsState): The current state.

        Returns:
            The updated state.
        """
        index = (
            min(state.selected_index, len(action.gamerooms) - 1)
            if action.gamerooms
            else 0
        )
        return GameroomsState(
            rows=tuple(
                GameroomRowViewModel(gameroom, idx == index)
                for idx, gameroom in enumerate(action.gamerooms)
            ),
            selected_index=index,
        )


class ScrollGameroomsReducer(Reducer[ScrollGameroomsAction, GameroomsState]):
    """The reducer for the scroll gamerooms action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[ScrollGameroomsAction]:
        return ScrollGameroomsAction

    def apply(
        self, action: ScrollGameroomsAction, state: GameroomsState
    ) -> GameroomsState:
        """Apply the scroll gamerooms action.

        Updates the selected index based on the direction of the scroll.

        Args:
            action (ScrollGameroomsAction): The action to apply.
            state (GameroomsState): The current state.

        Returns:
            The updated state.
        """
        index = state.selected_index

        match action.direction:
            case ScrollDirection.UP:
                if index == 0 or index >= len(state.rows):
                    return state
                index -= 1
            case ScrollDirection.DOWN:
                if index >= len(state.rows) - 1:
                    return state
                index += 1

        return evolve(
            state,
            rows=tuple(
                gameroom.with_is_highlighted(idx == index)
                for idx, gameroom in enumerate(state.rows)
            ),
            selected_index=index,
        )
