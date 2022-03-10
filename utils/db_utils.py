import random
import re
from json import loads
from logging import error

from bot_components.firebase_manager import FirebaseApp


def get_json_data(path, log_error=True):
    """Restituisce il contenuto json di un file nello storage di firebase,
    simile a `json.load(...)`, ma basta specificare il nome del file json. Se c'è un
    errore nel download del file, restituisce un dizionario vuoto. Per esempio:

    `get_json_data("configs/risposte.json")`

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


def get_photo(path):
    sb = FirebaseApp.storage_bucket
    bbs = list(sb.list_blobs(prefix=path))[1:]
    b = random.choice(bbs)
    return b.download_as_bytes()


def _get_main_photo_folders():
    sb = FirebaseApp.storage_bucket
    image_blobs_list = sb.list_blobs(prefix="images/")
    return [x.name for x in image_blobs_list if re.fullmatch(r"images/\w+/", x.name)]


def get_photos_dict():
    folders = _get_main_photo_folders()
    sb = FirebaseApp.storage_bucket
    return {f: list(sb.list_blobs(prefix=f))[1:] for f in folders}
