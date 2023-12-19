class AuthService:
    """A service storing the current authorization token."""

    __slots__ = ("_token",)

    def __init__(self) -> None:
        self._token: str | None = None

    def save_token(self, token: str) -> None:
        """Store the authorization token.

        Args:
            token (str): The token to store.
        """
        self._token = token

    def get_token(self) -> str | None:
        """Return the current authorization token.

        Returns:
            The token if one is stored, `None` otherwise.
        """
        return self._token
