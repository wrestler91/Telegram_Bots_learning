from aiogram.types import Message
from lexicon.lexicon import LEXICON
from aiogram import Router
from keyboard.buttons import keyboard_game

router: Router = Router()
# Этот хэндлер будет срабатывать на оставшиеся неизвестные сообщения,

@router.message()
async def process_unknown(message: Message):
    await message.answer(text=LEXICON['unknown'])




