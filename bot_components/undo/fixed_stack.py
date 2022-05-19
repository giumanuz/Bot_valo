from typing import TypeVar, Generic

T = TypeVar('T')


class FixedStack(Generic[T]):
    def __init__(self, max_elements: int):
        self._stack = []
        self.max_elements = max_elements

    def push(self, state: T):
        if len(self._stack) == self.max_elements:
            self._stack.pop(0)
        self._stack.append(state)

    def pop(self) -> T:
        return self._stack.pop()

    def last(self) -> T:
        if self.is_empty():
            return None
        return self._stack[-1]

    def is_empty(self):
        return len(self._stack) == 0
