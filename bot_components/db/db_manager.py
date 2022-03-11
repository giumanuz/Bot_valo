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
    def files_in_directory(self, folder: str) -> list:
        ...

    @abstractmethod
    def folders_in_directory(self, folder: str) -> list:
        ...

    @abstractmethod
    def download_as_text(self, location) -> str:
        ...

    @abstractmethod
    def download_as_json(self, location) -> dict:
        ...

    @abstractmethod
    def download_as_photo(self, location) -> bytes:
        ...
