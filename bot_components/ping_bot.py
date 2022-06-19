import logging
import random
import re
from threading import Timer

import requests
import telegram
from telegram.ext import Dispatcher


class PingBot:
    SAVED_RESPONSE_FILENAME = "pingbot_res_{id}.html"
    DEFAULT_ALERT_TEXT = "L'url è stato aggiornato! {url}"
    NONCE_PATTERN = re.compile(r'nonce=".*?"')
    SCRIPT_PATTERN = re.compile(r'<script.*?>(.|\n)*?</script>')

    _bot: telegram.Bot
    _random = random.Random(145)

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        cls._bot = dispatcher.bot

    def __init__(self,
                 url_to_ping: str,
                 interval: int,
                 ping_id: str | int = None,
                 alert_text: str = None):
        if not ping_id:
            ping_id = self._random.randint(0, 100000000)
        self.active = False
        self.url_to_ping = url_to_ping
        self.interval = interval
        self.active_timer: Timer = None
        self.registered_chats = set()
        self.filename = self.SAVED_RESPONSE_FILENAME.format(id=ping_id)

        alert_text = alert_text or self.DEFAULT_ALERT_TEXT
        self.alert_text = alert_text.format(url=url_to_ping)

    def activate(self):
        if not self._bot:
            logging.warning("Bot not set in PingBot. "
                            "Did you initialize it with PingBot.init(dispatcher)?")
        self.active = True
        self.event_loop(self.ping)

    def deactivate(self):
        self.active = False
        if self.active_timer and self.active_timer.is_alive():
            self.active_timer.cancel()
        self.active_timer = None

    def event_loop(self, function, *args):
        if self.active:
            function(*args)
            self.active_timer = Timer(self.interval, self.event_loop, (function, *args))
            self.active_timer.start()

    def ping(self):
        response = requests.get(url=self.url_to_ping).text
        normalized_response = self.normalize_html(response)
        try:
            with open(self.filename, 'r') as f:
                saved_response = f.read()
            if normalized_response != saved_response:
                self.alert()
        except IOError:
            pass
        finally:
            with open(self.filename, 'w') as f:
                f.write(normalized_response)

    def alert(self):
        for chat_id in self.registered_chats:
            self._bot.send_message(chat_id=chat_id,
                                   text=self.alert_text)

    def register_chat(self, chat_id: int):
        self.registered_chats.add(chat_id)

    @classmethod
    def normalize_html(cls, html: str):
        nonce_free_text = re.sub(cls.NONCE_PATTERN, '', html)
        return re.sub(cls.SCRIPT_PATTERN, '', nonce_free_text)
