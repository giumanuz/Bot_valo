from queue import Queue
from random import randint

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CallbackQueryHandler, CallbackContext


class CheckableQueue(Queue):
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    __directions_cw: tuple = (RIGHT, DOWN, LEFT, UP)

    @classmethod
    def next_cw(cls, cur_direction):
        cur_dir_index = cls.__directions_cw.index(cur_direction)
        return cls.__directions_cw[(cur_dir_index + 1) % 4]

    @classmethod
    def next_ccw(cls, cur_direction):
        cur_dir_index = cls.__directions_cw.index(cur_direction)
        return cls.__directions_cw[(cur_dir_index - 1) % 4]


class Snake:
    active_snake_games = {}

    # Commands:
    STRAIGHT = 0
    ROTATE_LEFT = 1
    ROTATE_RIGHT = 2

    BLANK_CELL = '⬜'
    SNAKE_CELL = '🟩'
    FRUIT_CELL = '🟥'
    DEATH_CELL = '💀'

    __SNAKE_GRID_SIZE = 10

    BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(text='↪️', callback_data='snake-1'),
            InlineKeyboardButton(text='⬆️', callback_data='snake-0'),
            InlineKeyboardButton(text='↩️', callback_data='snake-2')
        ]]
    )

    @classmethod
    def on_menu_entry_click(cls, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        if chat_id not in cls.active_snake_games:
            snake = Snake(chat_id, context)
            cls.active_snake_games[chat_id] = snake
            snake_game_message = context.bot.send_message(
                chat_id=chat_id,
                text=snake.to_string(),
                reply_markup=cls.BUTTONS
            )
            snake.set_message(snake_game_message)
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text="In questa chat c'è già un gioco attivo"
            )

    @classmethod
    def on_button_click(cls, update: Update, _):
        command = int(update.callback_query.data[6])
        chat_id = update.effective_chat.id
        snake_game: Snake = cls.active_snake_games.get(chat_id, None)
        if snake_game is None or not snake_game.game_active:
            return
        update.callback_query.answer()
        snake_game.change_direction(command)
        snake_game.go()
        cls.__update_message(snake_game, update)

    def __init__(self, chat_id, context):
        self.bot = context.bot
        self.chat_id = chat_id
        self.message = None

        self.direction = Direction.RIGHT
        self.snake_queue = CheckableQueue()
        self.pos = (0, 1)
        self.fruit = (3, 3)
        self.grid = [[self.BLANK_CELL for _ in range(self.__SNAKE_GRID_SIZE)] for _ in range(self.__SNAKE_GRID_SIZE)]
        self.game_active = True

        self.snake_queue.put(self.pos)
        self._insert_snake_pos_to_grid(self.pos)
        self._push_fruit_into_grid()

    def set_message(self, message):
        self.message = message

    def go(self):
        self.move_snake()
        if not self.game_active:
            return
        if self.pos == self.fruit:
            self.generate_new_fruit()
            return
        self.pop_snake_position()

    def change_direction(self, command):
        if command == self.STRAIGHT:
            return
        elif command == self.ROTATE_LEFT:
            self.direction = Direction.next_ccw(self.direction)
        elif command == self.ROTATE_RIGHT:
            self.direction = Direction.next_cw(self.direction)
        else:
            raise ValueError("Command not valid")

    def to_string(self):
        return '\n'.join((''.join(x) for x in self.grid))

    def lose(self):
        self.game_active = False
        self.message.edit_reply_markup(reply_markup=None)
        self.active_snake_games.pop(self.chat_id, None)
        self.bot.send_message(
            text="Hai perso!",
            chat_id=self.chat_id
        )

    def move_snake(self):
        old_x, old_y = self.pos
        dir_x, dir_y = self.direction
        self.pos = (old_x + dir_x, old_y + dir_y)

        if self.boundary_hit() or self.pos in self.snake_queue:
            self.lose()
            self._set_death_cell(old_x, old_y)
            return

        self.snake_queue.put(self.pos)
        self._insert_snake_pos_to_grid(self.pos)

    def pop_snake_position(self):
        old_pos = self.snake_queue.get()
        self._pop_snake_pos_from_grid(old_pos)

    def boundary_hit(self):
        return any((x < 0 or x >= 10 for x in self.pos))

    def generate_new_fruit(self):
        new_pos = self.__random_position()
        while new_pos in self.snake_queue:
            new_pos = self.__random_position()
        self.fruit = new_pos
        self._push_fruit_into_grid()

    @classmethod
    def __random_position(cls) -> tuple[int, int]:
        return randint(0, cls.__SNAKE_GRID_SIZE - 1), \
               randint(0, cls.__SNAKE_GRID_SIZE - 1)

    @classmethod
    def __update_message(cls, snake_game, update):
        update.callback_query.edit_message_text(
            text=snake_game.to_string()
        )
        if snake_game.game_active:
            update.callback_query.edit_message_reply_markup(
                reply_markup=cls.BUTTONS
            )

    def _insert_snake_pos_to_grid(self, position: tuple[int, int]):
        self.__set_grid_cell(position, self.SNAKE_CELL)

    def _pop_snake_pos_from_grid(self, position: tuple[int, int]):
        self.__set_grid_cell(position, self.BLANK_CELL)

    def _push_fruit_into_grid(self):
        self.__set_grid_cell(self.fruit, self.FRUIT_CELL)

    def _set_death_cell(self, x, y):
        self.__set_grid_cell((x, y), self.DEATH_CELL)

    def __set_grid_cell(self, position: tuple[int, int], cell_type: str):
        x, y = position
        self.grid[y][x] = cell_type


def init_snake(dispatcher: Dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(
        Snake.on_menu_entry_click, pattern="snake-callback"
    ))
    dispatcher.add_handler(CallbackQueryHandler(
        Snake.on_button_click, pattern="snake-[012]"
    ))
