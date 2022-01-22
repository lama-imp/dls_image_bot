import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types

from src.model.StyleTransfer import StyleTransfer
from src.bot.config import API_TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, loop=loop)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=types.ContentType.ANY)
async def echo(message: types.Message):
    print(message.photo[-1].file_id)
    content_name = 'content_{}.jpg'.format(message.from_user.id)
    await bot.download_file_by_id(message.photo[-1].file_id, content_name)

    style_path = 'style2.jpg'
    content_path = content_name

    s_transfer = StyleTransfer(style_path, content_path)
    task1 = asyncio.create_task(s_transfer.run_style_transfer())
    await task1
    s_transfer.save_image('output_{}.jpg'.format(message.from_user.id))
    output = types.InputFile('output_{}.jpg'.format(message.from_user.id))

    await message.answer_photo(output)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)