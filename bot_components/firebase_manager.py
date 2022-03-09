import firebase_admin
import firebase_admin.storage as fbs


class FirebaseApp:
    app: firebase_admin.App = None
    storage_bucket: fbs.storage.Bucket = None

    @classmethod
    def set_storage_bucket(cls, name):
        cls.storage_bucket = fbs.bucket(name)
