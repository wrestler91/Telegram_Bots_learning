from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU
from aiogram import Router

# Инициализируем роутер уровня модуля
router: Router = Router()

# срабатывает на команду /start
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])

# срабатывает на команду /help
@router.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])
