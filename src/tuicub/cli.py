import argparse
import asyncio
import pathlib
import tempfile

from .common.config import Config
from .tuicub import run


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="tuicub",
        description="An online multiplayer board game in your terminal.",
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Enable debug mode.",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-u",
        "--api-url",
        help="Base URL for the API.",
        action="store",
        required=False,
        metavar="URL",
        default="https://api.tuicub.com",
    )
    parser.add_argument(
        "--events-host",
        help="Hostname of the events server.",
        action="store",
        required=False,
        metavar="HOST",
        default="api.tuicub.com",
    )
    parser.add_argument(
        "--events-port",
        help="Port of the events server.",
        action="store",
        required=False,
        metavar="PORT",
        type=int,
        default="23432",
    )

    default_logfile = pathlib.Path(tempfile.gettempdir()) / "tuicub.log"
    parser.add_argument(
        "--logfile",
        help="If debug is enabled, write logs to file at this path.",
        action="store",
        required=False,
        metavar="PATH",
        default=default_logfile,
        type=pathlib.Path,
    )
    parser.add_argument(
        "--theme",
        help="Path to the file containing the custom color theme.",
        action="store",
        required=False,
        metavar="PATH",
        default=None,
        type=pathlib.Path,
    )
    parsed = parser.parse_args()

    config = Config(
        api_url=parsed.api_url,
        debug=parsed.debug,
        events_host=parsed.events_host,
        events_port=parsed.events_port,
        logfile=parsed.logfile,
        theme_file=parsed.theme,
    )

    return asyncio.run(run(config=config))
