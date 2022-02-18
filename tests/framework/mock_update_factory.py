from .mocks import MockUpdate, MockMessage


class MockUpdateFactory:
    @staticmethod
    def with_message(message: str):
        return MockUpdate(MockMessage(message))

    @staticmethod
    def empty():
        return MockUpdate()
