from telegram import Update, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, \
    CommandHandler, CallbackContext

from bot_components.db.db_manager import Database
from bot_components.settings.menu_setting import MenuSetting
from utils.lib_utils import FlowMatrix


class CrossChatMessagingSetting(MenuSetting):
    __MATRIX_ROW_LENGTH = 2
    CMD_REGISTRA = "registra"
    CMD_RIMUOVI = "rimuovi"
    CMD_MANDA = "manda"
    CMD_ANNULLA = "annulla"

    @property
    def name(self):
        return "Cross-Messages 🔀"

    @property
    def id(self):
        return "cross-chat-messaging-setting"

    def __init__(self, dispatcher: Dispatcher):
        super().__init__(dispatcher)
        self.command_matrix: InlineKeyboardMarkup = None
        self.setup_command_matrix()
        self.add_handlers()

    def setup_command_matrix(self):
        btn_registra = self.new_button("Registra chat", self.CMD_REGISTRA)
        btn_rimuovi = self.new_button("Rimuovi chat", self.CMD_RIMUOVI)
        btn_manda = self.new_button("Manda messaggio", self.CMD_MANDA)
        btn_annulla = self.new_button("Annulla", self.CMD_ANNULLA)
        flow_matrix = FlowMatrix(row_length=self.__MATRIX_ROW_LENGTH)
        flow_matrix.append(btn_registra)
        flow_matrix.append(btn_rimuovi)
        flow_matrix.append(btn_manda)
        flow_matrix.append(btn_annulla)
        self.command_matrix = InlineKeyboardMarkup(flow_matrix.list)

    def add_handlers(self):
        self.dispatcher.add_handler(ConversationHandler(
            entry_points=[CallbackQueryHandler(self.inserisci_alias_chat, pattern=self.pattern(self.CMD_REGISTRA))],
            states={
                0: [MessageHandler(Filters.text & ~Filters.command, self.registra_chat)]
            },
            fallbacks=[CommandHandler("quit", self.annulla, ~Filters.update.edited_message)]
        ))
        self.add_callback_query_handler(self.rimuovi_chat, self.CMD_RIMUOVI)
        self.dispatcher.add_handler(ConversationHandler(
            entry_points=[CallbackQueryHandler(self.scegli_alias, pattern=self.pattern(self.CMD_MANDA))],
            states={
                0: [CallbackQueryHandler(self.inserisci_messaggio, pattern=self.pattern("alias", r"-?\d+"))],
                1: [MessageHandler(Filters.text & ~Filters.command, self.invia_messaggio)]
            },
            fallbacks=[CommandHandler("quit", self.annulla, ~Filters.update.edited_message)]
        ))
        self.add_callback_query_handler(self.rimuovi_chat, self.CMD_RIMUOVI)
        self.add_callback_query_handler(self.annulla, self.CMD_ANNULLA)

    def callback(self, update: Update, _):
        update.effective_message.edit_text(
            "Scegli azione:",
            reply_markup=self.command_matrix
        )

    @staticmethod
    def inserisci_alias_chat(update: Update, _):
        update.effective_message.edit_text("Inserisci il nome della chat:")
        return 0

    @staticmethod
    def registra_chat(update: Update, _):
        existing_aliases = Database.get().get_chat_aliases()
        new_alias = update.message.text
        this_chat = update.effective_chat
        for alias, chat_id in existing_aliases.items():
            if chat_id == this_chat.id:
                this_chat.send_message(f"Chat già registrata come '{alias}'.")
                return ConversationHandler.END
            if alias == new_alias.lower():
                this_chat.send_message("Questo nome già esiste, scegline un altro.")
                return 0
        Database.get().set_chat_alias(new_alias, this_chat.id)
        this_chat.send_message("Chat registrata correttamente")
        return ConversationHandler.END

    @staticmethod
    def rimuovi_chat(update: Update, _):
        existing_aliases = Database.get().get_chat_aliases()
        for alias, chat_id in existing_aliases.items():
            if chat_id == update.effective_chat.id:
                Database.get().remove_chat_alias(alias)
                update.effective_message.edit_text("Chat rimossa correttamente")
                return
        update.effective_message.edit_text("La chat non è registrata.")

    def scegli_alias(self, update: Update, _):
        existing_aliases = Database.get().get_chat_aliases()
        matrix = FlowMatrix(row_length=2)
        for alias, chat_id in existing_aliases.items():
            if chat_id == update.effective_chat.id:
                continue
            btn = self.new_button(alias, "alias", chat_id)
            matrix.append(btn)
        if matrix.is_empty():
            update.effective_message.edit_text("Non ci sono altre chat a cui inviare messaggi.")
            return ConversationHandler.END
        update.effective_message.edit_text(
            "Scegli la chat:",
            reply_markup=InlineKeyboardMarkup(matrix.list)
        )
        return 0

    @staticmethod
    def inserisci_messaggio(update: Update, context: CallbackContext):
        tokens = update.callback_query.data.split("-")
        chat_id = int(tokens[-1]) * (-1 if tokens[-2] == "" else 1)
        context.chat_data["selected_chat_id"] = chat_id
        update.effective_message.edit_text("Inserisci il messaggio che vuoi inviare:")
        return 1

    @staticmethod
    def invia_messaggio(update: Update, context: CallbackContext):
        try:
            chat_id = context.chat_data["selected_chat_id"]
            message = update.message.text
            context.bot.send_message(chat_id=chat_id, text=message)
            update.effective_chat.send_message("Messaggio inviato correttamente.")
        except KeyError:
            update.effective_chat.send_message("Si è verificato un errore. Riprova.")
        finally:
            return ConversationHandler.END

    @staticmethod
    def annulla(update: Update, _):
        if update.effective_message.reply_markup:
            update.effective_message.edit_text("Azione annullata correttamente.")
        else:
            update.effective_chat.send_message("Azione annullata correttamente.")
        return ConversationHandler.END
