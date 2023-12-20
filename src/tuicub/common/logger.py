import atexit
from io import TextIOWrapper
from pathlib import Path

import httpx
import structlog
from attr import asdict
from attrs import has
from pydepot import Action


class Logger:
    """A logging interface wrapping the `structlog`."""

    __slots__ = ("_logfile_path", "_logfile", "_debug", "__weakref__")

    def __init__(self, logfile_path: Path, debug: bool):
        """Initialize new logger.

        Args:
            logfile_path (Path): The path to the file to write logs to.
            debug (bool): Is the logger in debug mode.
        """
        self._logfile_path: Path = logfile_path
        self._logfile: TextIOWrapper | None = None
        self._debug: bool = debug

    def configure(self) -> None:
        """Configure the logger."""
        logfile = open(self._logfile_path, "a")  # noqa: SIM115
        atexit.register(logfile.close)
        self._logfile = logfile

        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.ExceptionRenderer(
                    structlog.tracebacks.ExceptionDictTransformer(max_frames=3)
                ),
                structlog.processors.TimeStamper(fmt="iso", key="ts"),
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.WriteLoggerFactory(file=logfile),
        )

    def log_action(self, action: Action) -> None:
        """Log a store action."""
        if not self._debug:
            return

        log = structlog.get_logger()
        action_name = type(action).__name__
        params: dict = {}
        if has(type(action)):
            params = asdict(action, retain_collection_types=False)  # type: ignore

        log.info("action_dispatch", action_name=action_name, **params)

    def log_http_request(self, request: httpx.Request) -> None:
        """Log an http request."""
        if not self._debug:
            return

        log = structlog.get_logger()
        log.info("http_request", method=request.method, path=request.url.path)

    def log_http_response(self, response: httpx.Response) -> None:
        """Log an http response."""
        if not self._debug:
            return

        log = structlog.get_logger()
        log.info(
            "http_response",
            method=response.request.method,
            path=response.request.url.path,
            code=response.status_code,
        )
