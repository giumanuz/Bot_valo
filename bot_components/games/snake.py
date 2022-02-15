from queue import Queue
from random import randint
from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Message
from telegram.ext import Dispatcher, CallbackQueryHandler, CallbackContext, Job


class CheckableQueue(Queue):
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


class Snake:
    active_snake_games = {}
    # Commands:
    GO_UP = 0
    GO_DOWN = 1
    GO_LEFT = 2
    GO_RIGHT = 3

    # Directions:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    BLANK_CELL = '⬜'
    SNAKE_CELL = '🟩'
    FRUIT_CELL = '🟥'
    DEATH_CELL = '💀'

    __SNAKE_GRID_SIZE = 10
    __SNAKE_GRID_SIZE_GROUP = 7

    BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(text='⬆️', callback_data=f'snake-{GO_UP}'),
        ], [
            InlineKeyboardButton(text='⬅️', callback_data=f'snake-{GO_LEFT}'),
            InlineKeyboardButton(text='⬇️', callback_data=f'snake-{GO_DOWN}'),
            InlineKeyboardButton(text='➡️', callback_data=f'snake-{GO_RIGHT}'),
        ]])

    @classmethod
    def on_menu_entry_click(cls, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        if chat_id not in cls.active_snake_games:
            from telegram import Chat
            if update.effective_chat.type == Chat.PRIVATE:
                snake = Snake(chat_id, context, is_group=False)
                interval = 0.7
            else:
                snake = Snake(chat_id, context, is_group=True)
                interval = 3.05
                context.bot.send_message(text="Lo snake è lento nei gruppi. Provalo in chat privata!", chat_id=chat_id)
            cls.active_snake_games[chat_id] = snake
            snake_game_message = context.bot.send_message(
                chat_id=chat_id,
                text=snake.to_string(),
                reply_markup=cls.BUTTONS
            )
            snake.set_message(snake_game_message)
            job = context.job_queue.run_repeating(snake.update, interval=interval)
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

    def __init__(self, chat_id: int, context: CallbackContext, is_group: bool = False):
        self.context = context
        self.update_loop_job: Optional[Job] = None
        self.chat_id = chat_id
        self.message: Optional[Message] = None

        self.direction = self.RIGHT
        self.snake_queue = CheckableQueue()
        self.pos = (1, 1)
        self.fruit = (3, 3)
        self.game_size = self.__SNAKE_GRID_SIZE_GROUP if is_group else self.__SNAKE_GRID_SIZE
        self.grid = [[self.BLANK_CELL for _ in range(self.game_size)] for _ in range(self.game_size)]
        self.game_active = True
        self.points = 0

        self.snake_queue.put(self.pos)
        self._insert_snake_pos_to_grid(self.pos)
        self._push_fruit_into_grid()

    def set_job(self, job):
        self.update_loop_job = job

    def set_message(self, message):
        self.message = message

    def update(self, _):
        self.go()
        self.__update_message()

    def go(self):
        self.move_snake()
        if not self.game_active:
            return
        if self.pos == self.fruit:
            self.generate_new_fruit()
            return
        self.pop_snake_position()

    def change_direction(self, command):
        if command == self.GO_UP:
            self.direction = self.UP
        elif command == self.GO_DOWN:
            self.direction = self.DOWN
        elif command == self.GO_LEFT:
            self.direction = self.LEFT
        elif command == self.GO_RIGHT:
            self.direction = self.RIGHT
        else:
            raise ValueError("Command not valid")

    def to_string(self):
        return '\n'.join((''.join(x) for x in self.grid))

    def lose(self):
        self.update_loop_job.schedule_removal()
        self.game_active = False
        self.message.edit_reply_markup(reply_markup=None)
        self.active_snake_games.pop(self.chat_id, None)
        self.context.bot.send_message(
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
        return any((x < 0 or x >= self.game_size for x in self.pos))

    def generate_new_fruit(self):
        new_pos = self.__random_position()
        while new_pos in self.snake_queue:
            new_pos = self.__random_position()
        self.fruit = new_pos
        self._push_fruit_into_grid()

    def __random_position(self) -> tuple[int, int]:
        return randint(0, self.game_size - 1), \
               randint(0, self.game_size - 1)

    def __update_message(self):
        reply_markup = self.BUTTONS if self.game_active else None
        self.message.edit_text(
            text=self.to_string(),
            reply_markup=reply_markup
        )

    def add_points(self):
        self.points += 10

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
        Snake.on_menu_entry_click, pattern="snake-callback", run_async=True
    ))
    dispatcher.add_handler(CallbackQueryHandler(
        Snake.on_button_click, pattern="snake-[0123]", run_async=True
    ))
