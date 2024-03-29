from pytest import fixture

from botvalo_tests.test_utilities.common_tests_utils import GET_COMMON_BOT


@fixture
def simple_setup():
    GET_COMMON_BOT().reset_data()


# noinspection PyProtectedMember
@fixture
def full_blacklist():
    from bot_components.foto import Foto
    GET_COMMON_BOT().reset_data()
    Foto._full_blacklist()
    yield
    Foto._init_blacklist()


# noinspection PyProtectedMember
@fixture
def empty_blacklist():
    from bot_components.foto import Foto
    GET_COMMON_BOT().reset_data()
    Foto._empty_blacklist()
    yield
    Foto._init_blacklist()
