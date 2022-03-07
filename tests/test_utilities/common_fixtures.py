import pytest

from tests.test_utilities.common_tests_utils import GET_COMMON_BOT


@pytest.fixture
def setup():
    GET_COMMON_BOT().reset_data()


# noinspection PyProtectedMember
@pytest.fixture
def full_blacklist():
    from bot_components.foto import Foto
    GET_COMMON_BOT().reset_data()
    Foto._full_blacklist()
    yield
    Foto._init_blacklist()


# noinspection PyProtectedMember
@pytest.fixture
def empty_blacklist():
    from bot_components.foto import Foto
    GET_COMMON_BOT().reset_data()
    Foto._empty_blacklist()
    yield
    Foto._init_blacklist()
