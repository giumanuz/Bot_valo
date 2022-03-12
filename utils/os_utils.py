def get_absolute_path(path_as_main: str = None) -> str:
    """Prende in input una stringa che rappresenta il percorso al file voluto,
    partendo dalla directory del main. Per esempio, per ottenere il percorso
    al file `dichiarazione.json` dentro la cartella `prenotazioni` dentro `resources`,
    basta mettere in input la stringa \"`/resources/prenotazioni/dichiarazione.json`\"."""
    from os.path import join, dirname
    if path_as_main is None:
        return join(dirname(__file__), "../bot_components", "..")
    tokens = path_as_main.strip().split('/')
    if tokens[0] in ('.', ''):
        tokens = tokens[1:]
    return join(dirname(__file__), "../bot_components", "..", *tokens)


def get_current_local_datetime():
    """Restituisce l'oggetto `datetime.datetime` dell'orario al momento della chiamata
    a funzione, nel fuso orario italiano."""
    from datetime import datetime
    from pytz import utc, timezone
    local_timezone = timezone("Europe/Rome")
    return utc.localize(datetime.utcnow()).astimezone(local_timezone)


def get_current_weekday_name(local_datetime=None):
    """Restituisce il nome del giorno della settimana attuale, in inglese, in minuscolo.
    Per esempio, restituisce 'monday' se oggi è Lunedì. Sincronizzato col fuso orario
    italiano. Se viene specificato `local_datetime`, userà quella invece dell'orario al
    momento della chiamata."""
    from datetime import datetime
    if local_datetime is None:
        local_datetime = get_current_local_datetime()
    return datetime.strftime(local_datetime, "%A").lower()
