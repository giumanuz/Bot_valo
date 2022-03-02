def get_effective_text(update):
    if update.effective_message.caption is not None:
        text = str(update.effective_message.caption).lower()
    else:
        text = str(update.effective_message.text).lower()
    return text
