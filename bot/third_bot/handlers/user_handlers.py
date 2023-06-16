from aiogram.types import Message
from aiogram.filters import Command, CommandStart, Text
from lexicon.lexicon import LEXICON_RU
from aiogram import Router
from keyboard.buttons import keyboard_start, keyboard_game
from services.symbol_choice import get_choice, get_winner

# Инициализируем роутер уровня модуля
router: Router = Router()

# срабатывает на команду /start
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=keyboard_start)


# срабатывает на команду /help
@router.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'],
                         reply_markup=keyboard_start)


# срабатывает во время игры на нажатие одной из кнопок игры.
@router.message(Text(text=['Камень', 'Ножницы', 'Бумага']))
async def process_rock(message: Message):
    bot_choice = get_choice()
    await message.answer(text = f'Мой выбор {bot_choice}')
    player_choice = message.text
    winner = get_winner(bot_choice, player_choice)
    if winner:
        await message.answer(text = f'{winner} победил\n'
                             'Сыграем еще разок?',
                             reply_markup=keyboard_start)
    else:
        await message.answer(text = LEXICON_RU['duce'],
                             reply_markup=keyboard_game)


# Хендлер срабатывает на при нажатии на кнопку "Давай"
@router.message(Text(text='Давай'))
async def start_game(message: Message):
    await message.answer(text = LEXICON_RU['Yes'],
                         reply_markup=keyboard_game)


# Хендлер срабатывает на при нажатии на кнопку "Не хочу"
@router.message(Text(text='Не хочу'))
async def start_game(message: Message):
    await message.answer(text = LEXICON_RU['No'])
