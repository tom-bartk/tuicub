from pydepot import Store

from ...app.state import AppState


class ConfirmInteractor:
    """The interactor for answering confirmations."""

    __slots__ = ("_store",)

    def __init__(self, store: Store[AppState]):
        """Initialize new interactor.

        Args:
            store (Store[AppState]): The store of the app state.
        """
        self._store: Store[AppState] = store

    def answer_confirmation(self, answer: bool) -> None:
        """Answer the currently displayed confirmation.

        Args:
            answer (bool): Whether the confirmation is rejected, or confirmed.
        """
        if confirmation := self._store.state.confirmation:
            confirmation.answer(answer)
