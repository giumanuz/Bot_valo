from botvalo_tests.framework.mockchat import MockChat
from botvalo_tests.framework.mockmessage import MockMessage

COMMON_BOT = None


# noinspection PyProtectedMember
def SET_COMMON_BOT(bot):
    global COMMON_BOT
    COMMON_BOT = bot
    MockMessage._SET_COMMON_BOT(bot)
    MockChat._SET_COMMON_BOT(bot)


def GET_COMMON_BOT():
    global COMMON_BOT
    return COMMON_BOT


def send_fake_message_to(cls, text):
    cls.handle_message(text, MockChat.common())


def has_valid_photo(res, index=0):
    return 'photo' in res[index] and len(res[index]['photo']) != 0
