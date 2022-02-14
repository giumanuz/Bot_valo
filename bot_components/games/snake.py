from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CallbackQueryHandler, CallbackContext


class Snake:
    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(text='↪️', callback_data='snake-1'),
            InlineKeyboardButton(text='⬆️', callback_data='snake-0'),
            InlineKeyboardButton(text='↩️', callback_data='snake-2')
        ]]
    )

    @classmethod
    def handle_command(cls, update: Update, context: CallbackContext):
        message_id = update.effective_message.message_id
        if message_id not in active_snake_games:
            snake = Snake()
            active_snake_games[message_id] = snake
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=snake.to_string(),
                reply_markup=cls.buttons
            )

    @staticmethod
    def handle_callback(update: Update, context: CallbackContext):
        update.callback_query.answer()
        print(update.callback_query.data)

    def to_string(self):
        return '⬜⬜⬜⬜⬜'


active_snake_games = {}


def init_snake(dispatcher: Dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(
        Snake.handle_command, pattern="snake-callback"
    ))
    dispatcher.add_handler(CallbackQueryHandler(
        Snake.handle_callback, pattern="snake-[012]"
    ))
