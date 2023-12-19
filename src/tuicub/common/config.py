import pathlib

from attrs import field, frozen


@frozen
class Config:
    """A configuration for the application.

    Attributes:
        api_url (str): The URL to use for the tuicub API.
        debug (bool): A debug flag enabling various debugging features.
        events_host (str): The host of the events server.
        events_port (str): The port of the events server.
        logfile (pathlib.Path): The path to the file to write logs to.
        theme_file (pathlib.Path): An optional path to a file with a custom color theme.
    """

    api_url: str
    debug: bool
    events_host: str
    events_port: int
    logfile: pathlib.Path
    theme_file: pathlib.Path | None = field(default=None)
