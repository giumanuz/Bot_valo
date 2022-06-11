import os
import random

from firebase_admin import firestore, App, initialize_app, storage
from firebase_admin.credentials import Certificate

from bot_components.db.db_manager import Database


class FirebaseStorage(Database):
    _app: App = None
    _storage_bucket: storage.storage.Bucket = None
    _firestore_client: firestore.firestore.Client = None

    credentials_dict = {
        "type": "service_account",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
    }

    @classmethod
    def init(cls):
        STORAGE_BUCKET_NAME = os.environ["FB_BUCKET_NAME"]
        cls._init_credentials()
        cred = Certificate(cls.credentials_dict)
        cls._app = initialize_app(cred)
        cls._firestore_client = firestore.client()
        cls._storage_bucket = storage.bucket(STORAGE_BUCKET_NAME)

    @classmethod
    def _init_credentials(cls):
        private_key = os.environ["FB_CREDENTIALS_PRIVATE_KEY"].replace('\\n', '\n')
        client_email = os.environ["FB_CLIENT_EMAIL"]
        cls.credentials_dict["project_id"] = os.environ["FB_PROJECT_ID"]
        cls.credentials_dict["private_key_id"] = os.environ["FB_CREDENTIALS_KEY_ID"]
        cls.credentials_dict["private_key"] = private_key
        cls.credentials_dict["client_id"] = os.environ["FB_CLIENT_ID"]
        cls.credentials_dict["client_email"] = client_email

    @classmethod
    def set_as_default_database(cls):
        Database._CURRENT_DB = FirebaseStorage

    def register_for_config_changes(self, document: str, callback):
        config_doc = self._get_config_doc(document)
        config_doc.on_snapshot(lambda x, y, z: callback())

    def _get_config_doc(self, document: str):
        configs = self._firestore_client.collection("configs")
        return configs.document(document)

    def _get_config_doc_as_dict(self, document: str):
        configs = self._firestore_client.collection("configs")
        document = configs.document(document)
        doc = document.get()
        if not doc.exists:
            raise FileNotFoundError()
        return doc.to_dict()

    def get_lista_insulti(self) -> list[str]:
        dict_insulti = self._get_config_doc_as_dict("insulti")
        lista_insulti = dict_insulti['insulti']
        return lista_insulti

    def get_chat_aliases(self) -> dict[str, int]:
        return self._get_config_doc_as_dict("alias_chat")

    def get_keyword_foto(self) -> dict[str, list[str]]:
        return self._get_config_doc_as_dict("keyword_foto")

    def get_nicknames(self) -> dict[int, str]:
        return self._get_config_doc_as_dict("nicknames")

    def get_risposte(self) -> dict[int, any]:
        return self._get_config_doc_as_dict("risposte")

    def get_schedule_blacklist(self) -> dict[str, list[str]]:
        return self._get_config_doc_as_dict("schedule_blacklist")

    def get_random_photo(self, category: str) -> bytes:
        blobs_in_directory = self._storage_bucket.list_blobs(
            prefix=f"images/{category}/"
        )
        photos_list = list(blobs_in_directory)[1:]
        random_photo = random.choice(photos_list)
        bts = random_photo.download_as_bytes()
        return bts

    def get_chat_removal_seconds(self, chat_id: int, default=5) -> dict:
        chat_id = str(chat_id)
        doc_data = self._get_config_doc_as_dict("chat_removal_seconds")
        return doc_data.get(chat_id, default)

    def set_chat_removal_seconds(self, chat_id: int, seconds: float):
        chat_id = str(chat_id)
        doc = self._get_config_doc("chat_removal_seconds")
        doc.update({chat_id: seconds})

    def set_chat_alias(self, name: str, chat_id: int):
        doc = self._get_config_doc("alias_chat")
        doc.update({f"`{name}`": chat_id})

    def remove_chat_alias(self, name: str):
        doc = self._get_config_doc("alias_chat")
        doc.update({f"`{name}`": firestore.firestore.DELETE_FIELD})

    def get_cioppy_blacklist_words(self) -> list[str]:
        words_dict = self._get_config_doc_as_dict("timeout")
        words_list: list[str] = words_dict['blacklisted_words']
        return words_list

    def _get_timeout_data(self, key):
        doc_data = self._get_config_doc_as_dict("timeout")
        return doc_data[key]

    def get_cioppy_bans(self) -> int:
        return self._get_timeout_data('bans')

    def set_cioppy_bans(self, ban_times):
        doc = self._get_config_doc("timeout")
        doc.update({"bans": ban_times})

    def get_cioppy_max_alerts(self) -> int:
        return self._get_timeout_data('max_alerts')

    def get_minimum_voters_required_to_ban_cioppy(self) -> int:
        return self._get_timeout_data('min_voters_required')

    def set_cioppy_decrease_ban_timestamp(self, timestamp):
        doc = self._get_config_doc("timeout")
        doc.update({"ban_decrease_timestamp": timestamp})

    def get_cioppy_decrease_ban_timestamp(self) -> float:
        return self._get_timeout_data('ban_decrease_timestamp')
