from logging import error

from bot_components.db.db_manager import Database


def get_json_data(path, log_error=True):
    """Restituisce il contenuto json di un file nello storage di firebase,
    simile a `json.load(...)`, ma basta specificare il nome del file json. Se c'è un
    errore nel download del file, restituisce un dizionario vuoto. Per esempio:

    `get_json_data("configs/risposte.json")`

    Se `log_error` = True (default), eventuali errori vengono loggati nella console.
    """
    try:
        # blob = FirebaseStorage.storage_bucket.get_blob(path)
        # json_str = blob.download_as_text()
        # parsed_json = loads(json_str)
        # return parsed_json
        db = Database.get()
        print(type(db))
        return db.download_as_json(path)
    except AttributeError as e:
        if log_error:
            error(f"Error downloading file {path}: {e}")
        return {}


def get_photos_dict():
    db = Database.get()
    folders = db.folders_in_directory("images")
    return {f: db.files_in_directory(f) for f in folders}
