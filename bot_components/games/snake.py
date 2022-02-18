import logging
from queue import Queue
from random import randint
from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Message, Chat
from telegram.ext import Dispatcher, CallbackQueryHandler, CallbackContext, Job


class CheckableQueue(Queue):
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue

    def __len__(self):
        with self.mutex:
            return self.queue.__len__()


class Snake:
    active_snake_games = {}

    # Commands
    GO_UP = 0
    GO_DOWN = 1
    GO_LEFT = 2
    GO_RIGHT = 3

    # Directions
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    # Cell types
    BLANK_CELL = '⬜'
    SNAKE_CELL = '🟩'
    HEAD_CELL = '🟢'
    FRUIT_CELL = '🟥'
    DEATH_CELL = '💀'

    # Snake settings
    __SNAKE_GRID_SIZE = 8
    __SNAKE_GRID_SIZE_GROUP = 6
    __UPDATE_INTERVAL = 1
    __UPDATE_INTERVAL_GROUP = 3.01  # Must be at least 3

    BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(text='⬆️', callback_data=f'snake-{GO_UP}'),
        ], [
            InlineKeyboardButton(text='⬅️', callback_data=f'snake-{GO_LEFT}'),
            InlineKeyboardButton(text='⬇️', callback_data=f'snake-{GO_DOWN}'),
            InlineKeyboardButton(text='➡️', callback_data=f'snake-{GO_RIGHT}'),
        ]])

    # Callback handling

    @classmethod
    def on_menu_entry_click(cls, update: Update, context: CallbackContext):
        logging.basicConfig(level=logging.DEBUG)
        chat_id = update.effective_chat.id
        if chat_id not in cls.active_snake_games:
            if update.effective_chat.type == Chat.PRIVATE:
                snake = Snake(chat_id, context, is_group=False)
                interval = cls.__UPDATE_INTERVAL
            else:
                snake = Snake(chat_id, context, is_group=True)
                interval = cls.__UPDATE_INTERVAL_GROUP
                context.bot.send_message(text="Lo snake è lento nei gruppi. Provalo in chat privata!", chat_id=chat_id)
            cls.active_snake_games[chat_id] = snake

            snake_game_message = cls.send_snake_message(chat_id, context, snake)
            snake.set_message(snake_game_message)
            job = context.job_queue.run_repeating(snake.go, interval=interval)
            snake.set_job(job)
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
        snake_game.change_direction(command)
        update.callback_query.answer()

    @classmethod
    def send_snake_message(cls, chat_id, context, snake):
        snake_game_message = context.bot.send_message(
            chat_id=chat_id,
            text=snake.to_string(),
            reply_markup=cls.BUTTONS
        )
        return snake_game_message

    # Instance init methods

    def __init__(self, chat_id: int, context: CallbackContext, is_group: bool = False):
        self.context = context
        self.update_loop_job: Optional[Job] = None
        self.chat_id = chat_id
        self.message: Optional[Message] = None
        self.game_active = True
        self.game_size = self.__SNAKE_GRID_SIZE_GROUP if is_group else self.__SNAKE_GRID_SIZE
        self.square_size = self.game_size * self.game_size
        self.grid = [[self.BLANK_CELL for _ in range(self.game_size)] for _ in range(self.game_size)]

        self.snake_queue = CheckableQueue()
        self.head_pos = (1, 1)
        self.cur_direction = self.RIGHT
        self.fruit_pos = None
        self.points = 0

        self._push_snake_position()
        self.generate_new_fruit()

    def set_job(self, job):
        self.update_loop_job = job

    def set_message(self, message):
        self.message = message

    # Instance methods

    def to_string(self) -> str:
        return '\n'.join(''.join(x) for x in self.grid)

    def go(self, _):
        self.move_snake()
        if not self.game_active:
            return
        if self.head_pos == self.fruit_pos:
            self.eat_fruit()
            self.__update_message()
            return
        self._pop_snake_position()
        self.__update_message()

    def move_snake(self):
        prev_position = self.head_pos
        old_x, old_y = prev_position
        dir_x, dir_y = self.cur_direction
        self.head_pos = (old_x + dir_x, old_y + dir_y)
        if self.boundary_hit() or self.head_pos in self.snake_queue:
            self.lose()
            self._set_death_cell(prev_position)
            return
        self._push_snake_position(prev_position)

    def change_direction(self, command):
        if command == self.GO_UP:
            self.cur_direction = self.UP
        elif command == self.GO_DOWN:
            self.cur_direction = self.DOWN
        elif command == self.GO_LEFT:
            self.cur_direction = self.LEFT
        elif command == self.GO_RIGHT:
            self.cur_direction = self.RIGHT
        else:
            raise ValueError("Command not valid")

    def eat_fruit(self):
        self.add_points()
        if len(self.snake_queue) == self.square_size:
            self.win()
        self.generate_new_fruit()

    def generate_new_fruit(self):
        new_pos = self._get_random_position()
        while new_pos in self.snake_queue:
            new_pos = self._get_random_position()
        self.fruit_pos = new_pos
        self.__set_grid_cell(self.fruit_pos, self.FRUIT_CELL)

    def boundary_hit(self) -> bool:
        return any(x < 0 or x >= self.game_size for x in self.head_pos)

    def add_points(self):
        self.points += 10

    def win(self):
        self.__deactivate_game()
        self.context.bot.send_message(
            text=f"⭐ Hai vinto! Complimenti! ⭐\nPunti totali: {self.points}",
            chat_id=self.chat_id
        )

    def lose(self):
        self.__deactivate_game()
        self.context.bot.send_message(
            text=f"Hai perso!\nPunti totalizzati: {self.points}",
            chat_id=self.chat_id
        )

    def _push_snake_position(self, prev_position: tuple[int, int] = None):
        self.snake_queue.put(self.head_pos)
        self.__set_grid_cell(self.head_pos, self.HEAD_CELL)
        if prev_position is not None:
            self.__set_grid_cell(prev_position, self.SNAKE_CELL)

    def _pop_snake_position(self):
        old_pos = self.snake_queue.get()
        self.__set_grid_cell(old_pos, self.BLANK_CELL)

    def _get_random_position(self) -> tuple[int, int]:
        return randint(0, self.game_size - 1), \
               randint(0, self.game_size - 1)

    def _set_death_cell(self, position: tuple[int, int]):
        self.__set_grid_cell(position, self.DEATH_CELL)
        self.__update_message()

    def __set_grid_cell(self, position: tuple[int, int], cell_type: str):
        x, y = position
        self.grid[y][x] = cell_type

    def __update_message(self):
        reply_markup = self.BUTTONS if self.game_active else None
        self.message.edit_text(
            text=self.to_string(),
            reply_markup=reply_markup
        )

    def __deactivate_game(self):
        self.update_loop_job.schedule_removal()
        self.game_active = False
        self.message.edit_reply_markup(reply_markup=None)
        self.active_snake_games.pop(self.chat_id, None)


def init_snake(dispatcher: Dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(
        Snake.on_menu_entry_click, pattern="snake-callback", run_async=True
    ))
    dispatcher.add_handler(CallbackQueryHandler(
        Snake.on_button_click, pattern="snake-[0123]", run_async=True
    ))
