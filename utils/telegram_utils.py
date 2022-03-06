def get_effective_text(update):
    """Restituisce il testo effettivo del messaggio
    contenuto in `update`."""
    if update.effective_message.caption is not None:
        return str(update.effective_message.caption).lower()
    elif update.effective_message.text is not None:
        return str(update.effective_message.text).lower()
