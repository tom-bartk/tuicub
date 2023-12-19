from attrs import field, frozen

from ..common.confirmation.confirmation import Confirmation


@frozen
class AppState:
    """The UI state of the application.

    Attributes:
        confirmation (Confirmation | None): An optional pending confirmation.
            None means there is no confirmation currently pending answer.
    """

    confirmation: Confirmation | None = field(default=None)
