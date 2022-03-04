from tests.framework.mockupdate import MockUpdate

COMMON_CONTEXT = None


def SET_COMMON_CONTEXT(context):
    global COMMON_CONTEXT
    COMMON_CONTEXT = context


def send_fake_message_to(cls, text):
    update = MockUpdate.from_message(text)
    cls.handle_message(update)


def has_valid_photo(res, index=0):
    return 'photo' in res[index] and len(res[index]['photo']) != 0
