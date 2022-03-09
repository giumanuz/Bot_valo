from json import loads
from logging import error

from bot_components.firebase_manager import FirebaseApp


def get_json_data_from_db(path, log_error=True):
    """Restituisce il contenuto json di un file nello storage di firebase,
    simile a `json.load(...)`, ma basta specificare il nome del file json. Se c'è un
    errore nel download del file, restituisce un dizionario vuoto. Per esempio:

    `get_json_data_from_db("configs/risposte.json")`

    Se `log_error` = True (default), eventuali errori vengono loggati nella console.
    """
    try:
        blob = FirebaseApp.storage_bucket.get_blob(path)
        json_str = blob.download_as_text()
        parsed_json = loads(json_str)
        return parsed_json
    except AttributeError as e:
        if log_error:
            error(f"Error downloading file {path}: {e}")
        return {}


def get_photo_from_db(path):
    # TODO
    blob = FirebaseApp.storage_bucket.get_blob(path)
    json_str = blob.download_as_text()
    parsed_json = loads(json_str)
    return parsed_json
