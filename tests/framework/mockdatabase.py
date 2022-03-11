from bot_components.db.db_manager import Database


class MockDatabase(Database):
    def __init__(self):
        self.lista_insulti = []
        self.keyword_foto = {}
        self.dict_nicknames = {}
        self.schedule_blacklist = {}

    def load_default_values(self):
        self.lista_insulti = [
            "{} questo è un test",
            "{} questo è un altro test"
        ]
        self.keyword_foto = {
            "cazzi": [
                "pene", "mazza", "cazzo"
            ]
        }

    def register_for_config_changes(self, document: str, callback):
        pass

    def get_lista_insulti(self) -> list[str]:
        pass

    def get_keyword_foto(self) -> dict[str, list[str]]:
        pass

    def get_nicknames(self) -> dict[int, str]:
        pass

    def get_risposte(self) -> dict[int, any]:
        pass

    def get_schedule_blacklist(self) -> dict[str, list[str]]:
        pass

    def get_random_photo(self, category: str) -> bytes:
        pass

    def get_chat_removal_seconds(self, chat_id: int, default=5) -> dict:
        pass

    def set_chat_removal_seconds(self, chat_id: int, seconds: float):
        pass
