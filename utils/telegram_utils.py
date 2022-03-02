def get_effective_text(update):
    if update.effective_message.caption is not None:
        return str(update.effective_message.caption).lower()
    elif update.effective_message.text is not None:
        return str(update.effective_message.text).lower()
