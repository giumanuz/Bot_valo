from abc import ABC, abstractmethod


class StateChange(ABC):
    @property
    @abstractmethod
    def requires_admin(self) -> bool:
        ...

    @property
    @abstractmethod
    def can_undo(self) -> bool:
        ...

    @abstractmethod
    def undo(self):
        ...
