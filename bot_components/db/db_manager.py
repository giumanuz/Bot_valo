from abc import ABC as ABSTRACT_CLASS, abstractmethod


class Database(ABSTRACT_CLASS):
    _CURRENT_DB: type = None
    _INSTANCE: 'Database' = None

    @classmethod
    def set_db_type(cls, db_cls: type):
        cls._CURRENT_DB = db_cls

    @classmethod
    def get(cls) -> 'Database':
        if cls._INSTANCE is None:
            cls._INSTANCE = cls._CURRENT_DB()
        return cls._INSTANCE

    @abstractmethod
    def register_for_config_changes(self, document: str, callback):
        ...

    @abstractmethod
    def get_lista_insulti(self) -> list[str]:
        ...

    @abstractmethod
    def get_chat_aliases(self) -> dict[str, str]:
        ...

    @abstractmethod
    def get_keyword_foto(self) -> dict[str, list[str]]:
        ...

    @abstractmethod
    def get_nicknames(self) -> dict[int, str]:
        ...

    @abstractmethod
    def get_risposte(self) -> dict[int, any]:
        ...

    @abstractmethod
    def get_schedule_blacklist(self) -> dict[str, list[str]]:
        ...

    @abstractmethod
    def get_random_photo(self, category: str) -> bytes:
        ...

    @abstractmethod
    def get_chat_removal_seconds(self, chat_id: int, default=5) -> dict:
        ...

    @abstractmethod
    def set_chat_removal_seconds(self, chat_id: int, seconds: float):
        ...

    @abstractmethod
    def set_chat_alias(self, name: str, chat_id: int):
        ...

    @abstractmethod
    def remove_chat_alias(self, name: str):
        ...

    @abstractmethod
    def get_cioppy_blacklist_words(self) -> list[str]:
        ...

    @abstractmethod
    def get_cioppy_bans(self) -> int:
        ...

    @abstractmethod
    def set_cioppy_bans(self, ban_times):
        ...

    @abstractmethod
    def get_cioppy_max_alerts(self) -> int:
        ...

    @abstractmethod
    def get_minimum_voters_required_to_ban_cioppy(self) -> int:
        ...

    @abstractmethod
    def set_cioppy_decrease_ban_timestamp(self, timestamp):
        ...

    @abstractmethod
    def get_cioppy_decrease_ban_timestamp(self) -> float:
        ...
