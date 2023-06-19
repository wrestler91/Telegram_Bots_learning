from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup

# Инициализируем объект билдера
kb_builder_game: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_start: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

button_yes: KeyboardButton = KeyboardButton(text='Давай')
button_no: KeyboardButton = KeyboardButton(text='Не хочу')
button_rock: KeyboardButton = KeyboardButton(text='Камень')
button_scissors: KeyboardButton = KeyboardButton(text='Ножницы')
button_paper: KeyboardButton = KeyboardButton(text='Бумага')

kb_builder_game.row(button_rock, button_scissors, button_paper, width=1)
kb_builder_start.row(button_yes, button_no)

keyboard_game: ReplyKeyboardMarkup = kb_builder_game.as_markup(
                                    resize_keyboard=True)


keyboard_start: ReplyKeyboardMarkup = kb_builder_start.as_markup(
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

