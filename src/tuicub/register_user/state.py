from attrs import evolve, field, frozen
from pydepot import Action, Reducer


@frozen
class RegisterUserState:
    """The local state of the register user screen.

    Attributes:
        name (str): The current text of the textfield.
    """

    name: str = field(default="")


@frozen
class SetNameAction(Action):
    """An intent to update the current name.

    Attributes:
        name (str): The name to set.
    """

    name: str


@frozen
class SetNameReducer(Reducer[SetNameAction, RegisterUserState]):
    """The reducer for the set name action."""

    @property
    def action_type(self) -> type[SetNameAction]:
        return SetNameAction

    def apply(self, action: SetNameAction, state: RegisterUserState) -> RegisterUserState:
        """Apply the set name action.

        Updates the name field of the state.

        Args:
            action (SetNameAction): The action to apply.
            state (RegisterUserState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, name=action.name)
