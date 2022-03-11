import os
import random

from firebase_admin import firestore, App, initialize_app, storage
from firebase_admin.credentials import Certificate

from bot_components.db.db_manager import Database
from utils.os_utils import get_absolute_path


class FirebaseStorage(Database):
    _app: App = None
    _storage_bucket: storage.storage.Bucket = None
    _firestore_client: firestore.firestore.Client = None

    @classmethod
    def init(cls, credentials_path):
        path = get_absolute_path(credentials_path)
        cred = Certificate(path)
        cls._app = initialize_app(cred)
        cls._firestore_client = firestore.client()
        STORAGE_BUCKET_NAME = os.environ["FIREBASE_BUCKET_NAME"]
        cls._storage_bucket = storage.bucket(STORAGE_BUCKET_NAME)

    @classmethod
    def set_as_default_database(cls):
        Database._CURRENT_DB = FirebaseStorage

    def register_for_config_changes(self, document: str, callback):
        config_doc = self._get_config_doc(document)
        config_doc.on_snapshot(lambda x, y, z: callback())
        print(f"Registered callback {callback.__name__} for changes in {document}")

    def _get_config_doc(self, document: str):
        configs = self._firestore_client.collection("configs")
        return configs.document(document)

    def _get_config_doc_as_dict(self, document: str):
        configs = self._firestore_client.collection("configs")
        document = configs.document(document)
        return document.get().to_dict()

    def get_lista_insulti(self) -> list[str]:
        doc_insulti = self._get_config_doc("insulti")
        dict_insulti = doc_insulti.get(['insulti']).to_dict()
        lista_insulti = dict_insulti['insulti']
        return lista_insulti

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
        doc = self._get_config_doc("chat_removal_seconds")
        return doc.get().to_dict().get(chat_id, default)

    def set_chat_removal_seconds(self, chat_id: int, seconds: float):
        chat_id = str(chat_id)
        doc = self._get_config_doc("chat_removal_seconds")
        doc.update({chat_id: seconds})
