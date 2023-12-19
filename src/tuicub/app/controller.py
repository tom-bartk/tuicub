from prompt_toolkit.key_binding import KeyPressEvent

from ..common.confirmation import ConfirmInteractor


class AppController:
    """Captures and converts user input to interactions in the global app context."""

    __slots__ = ("_confirm_interactor",)

    def __init__(self, confirm_interactor: ConfirmInteractor):
        """Initialize new controller.

        Args:
            confirm_interactor (ConfirmInteractor): The interactor for confirmations.
        """
        self._confirm_interactor: ConfirmInteractor = confirm_interactor

    def answer_confirmation_yes(self, event: KeyPressEvent) -> None:
        """Handler for the confirm keybind.

        Confirms the currently pending confirmation.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._confirm_interactor.answer_confirmation(answer=True)

    def answer_confirmation_no(self, event: KeyPressEvent) -> None:
        """Handler for the reject keybind.

        Rejects the currently pending confirmation.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._confirm_interactor.answer_confirmation(answer=False)
