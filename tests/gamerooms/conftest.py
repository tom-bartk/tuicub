from unittest.mock import create_autospec

import pytest
from pydepot import Store

from src.tuicub.gamerooms.state import GameroomsState


@pytest.fixture()
def local_store() -> Store[GameroomsState]:
    return create_autospec(Store)
