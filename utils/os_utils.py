from os.path import join, dirname


def get_absolute_path(path_as_main: str = None) -> str:
    """Prende in input una stringa che rappresenta il percorso al file voluto,
    partendo dalla directory del main. Per esempio, per ottenere il percorso
    al file `dichiarazione.json` dentro la cartella `prenotazioni` dentro `resources`,
    basta mettere in input la stringa \"`/resources/prenotazioni/dichiarazione.json`\"."""
    if path_as_main is None:
        return join(dirname(__file__), "../bot_components", "..")
    tokens = path_as_main.strip().split('/')
    if tokens[0] in ('.', ''):
        tokens = tokens[1:]
    return join(dirname(__file__), "../bot_components", "..", *tokens)


def path_to_text_file(filename: str) -> str:
    """Restituisce il percorso completo a un file partendo dal suo nome.

    **Nota:** Il file deve trovarsi dentro la cartella `resources/text_files`.

    Equivalente di `get_absolute_path(f"/resources/text_files/{filename}")`"""
    return get_absolute_path(f"resources/text_files/{filename}")
