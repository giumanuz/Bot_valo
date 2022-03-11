import json
import re

import firebase_admin
import firebase_admin.storage as fbs

from bot_components.db.db_manager import Database


class FirebaseStorage(Database):
    app: firebase_admin.App = None
    storage_bucket: fbs.storage.Bucket = None

    @classmethod
    def set_storage_bucket(cls, name: str):
        print("Storage bucket set")
        cls.storage_bucket = fbs.bucket(name)

    def download_as_text(self, location) -> str:
        blob = self.storage_bucket.get_blob(location)
        return blob.download_as_text()

    def download_as_json(self, location) -> dict:
        blob = self.storage_bucket.get_blob(location)
        json_str = blob.download_as_text()
        return json.loads(json_str)

    def download_as_photo(self, location) -> bytes:
        # TODO: Ripensare il sistema di blob, perché dovrebbe essere come segue:
        #       blob = self.storage_bucket.get_blob(location)
        #       invece, files_in_directory(...) restituisce una lista di blob
        return location.download_as_bytes()

    def files_in_directory(self, folder: str) -> list:
        # TODO: Le cartelle sono cercate tramite regex, mentre questa implementazione
        #       non funziona se ci sono sottocartelle.
        elements = self.storage_bucket.list_blobs(prefix=f"{folder}/")
        files = list(elements)[1:]
        return files

    def folders_in_directory(self, folder: str) -> list:
        elements = self.storage_bucket.list_blobs(prefix=f"{folder}/")
        pattern_to_search = rf"{folder}/\w+/" if folder else r"\w+/"
        folders = [re.fullmatch(pattern_to_search, x.name) for x in elements]
        return folders
