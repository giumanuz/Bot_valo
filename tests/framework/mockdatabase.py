from bot_components.db.db_manager import Database


class MockDatabase(Database):
    def __init__(self):
        self.lista_insulti = []
        self.keyword_foto = {}
        self.dict_nicknames = {}
        self.schedule_blacklist = {}
        self.dict_risposte = {}
        self.removal_seconds = {}

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
        self.dict_nicknames = {"143938748": "Serchio"}
        self.schedule_blacklist = {}
        self.dict_risposte = {
            "grazie": "risposta_test",
            "ricorsione": "risposta_ricorsione",
            "ricorsivo": "ALT::ricorsione"
        }

    def register_for_config_changes(self, document: str, callback):
        callback()

    def get_lista_insulti(self) -> list[str]:
        return self.lista_insulti

    def get_keyword_foto(self) -> dict[str, list[str]]:
        return self.keyword_foto

    def get_nicknames(self) -> dict[int, str]:
        return self.dict_nicknames

    def get_risposte(self) -> dict[int, any]:
        return self.dict_risposte

    def get_schedule_blacklist(self) -> dict[str, list[str]]:
        return self.schedule_blacklist

    def get_random_photo(self, category: str) -> bytes:
        return b"random-photo"

    def get_chat_removal_seconds(self, chat_id: int, default=5) -> dict:
        return self.removal_seconds.get(str(chat_id), default)

    def set_chat_removal_seconds(self, chat_id: int, seconds: float):
        self.removal_seconds[str(chat_id)] = seconds
