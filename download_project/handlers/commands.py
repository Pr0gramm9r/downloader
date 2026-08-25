from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F

router = Router()

@router.message(Command("start"))
async def str_msg(message: Message):
    await message.answer('привет\n\ncommand_list:\n* /help - помощь\n* /download - скачивание')

@router.message(Command("help"))
async def help_msg(message: Message):
    await message.answer('хелпа😊👌👍\nв /download кидаешь ссылку и потом выбираешь что надо')