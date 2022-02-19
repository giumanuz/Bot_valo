from os.path import join, dirname


def get_absolute_path(path_as_main: str = None):
    if path_as_main is None:
        return join(dirname(__file__), "..", "..")
    tokens = path_as_main.strip().split('/')
    if tokens[0] in ('.', ''):
        tokens = tokens[1:]
    return join(dirname(__file__), "..", "..", *tokens)
