from aiogram import Bot, Dispatcher
from aiogram.types import Message
import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

@dp.message()
async def start_message(message: Message):
    await message.answer('привет')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())