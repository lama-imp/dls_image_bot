from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.model.StyleTransfer import StyleTransfer
from src.bot.config import BOT_TOKEN, start_image
from src.bot.messages import MESSAGES
from src.bot.utils import STStates


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    await bot.delete_webhook()


@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer_photo(start_image, caption=MESSAGES['start'])


@dp.message_handler(state='*', commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply(MESSAGES['help'])


@dp.message_handler(state='*', commands=['set_style'])
async def set_style_transfer(message: types.Message):
    await STStates.style.set()
    await message.reply(MESSAGES['style'])


@dp.message_handler(content_types=types.ContentType.PHOTO, state=STStates.style)
async def set_style_image(message: types.Message):
    style_name = 'style_{}.jpg'.format(message.from_user.id)
    await bot.download_file_by_id(message.photo[-1].file_id, style_name)
    await STStates.next()
    await bot.send_message(message.chat.id, MESSAGES['content'])


@dp.message_handler(content_types=types.ContentType.PHOTO, state=STStates.content)
async def img_style_transfer(message: types.Message):
    print(message.photo[-1].file_id)
    content_name = 'content_{}.jpg'.format(message.from_user.id)
    await bot.download_file_by_id(message.photo[-1].file_id, content_name)

    style_path = 'style_{}.jpg'.format(message.from_user.id)
    content_path = content_name

    s_transfer = StyleTransfer(style_path, content_path)
    s_transfer.run_style_transfer()
    s_transfer.save_image('output_{}.jpg'.format(message.from_user.id))
    output = types.InputFile('output_{}.jpg'.format(message.from_user.id))

    await message.answer_photo(output)


@dp.message_handler(content_types=types.ContentType.ANY, state=STStates.style)
async def not_supported_style(message: types.Message):
    await bot.send_message(message.chat.id, MESSAGES['not_supported_style'])


@dp.message_handler(content_types=types.ContentType.ANY, state=STStates.content)
async def not_supported_content(message: types.Message):
    await bot.send_message(message.chat.id, MESSAGES['not_supported_content'])


@dp.message_handler(content_types=types.ContentType.ANY, state=None)
async def unknown_message(message: types.Message):
    await bot.send_message(message.chat.id, MESSAGES['unknown'])


def start_bot():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
