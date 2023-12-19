import httpx

from ..config import Config
from ..logger import Logger


class TuicubHttpxClient(httpx.AsyncClient):
    """Async `httpx` client that logs requests and responses."""

    def __init__(self, config: Config, logger: Logger):
        self._logger: Logger = logger
        super().__init__(
            base_url=config.api_url,
            verify=False,
            event_hooks={"request": [self.log_request], "response": [self.log_response]},
        )

    async def log_request(self, request: httpx.Request) -> None:
        self._logger.log_http_request(request)

    async def log_response(self, response: httpx.Response) -> None:
        self._logger.log_http_response(response)
