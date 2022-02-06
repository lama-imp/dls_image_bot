import os
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from src.model.StyleTransfer import style_transfer_func
from src.bot.config import BOT_TOKEN, start_image
from src.bot.messages import MESSAGES
from src.bot.utils import STStates


loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN, loop=loop)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    '''
    This version uses polling so we need to delete webhook (if exists) on startup
    '''
    await bot.delete_webhook()


async def async_st(loop, style_transfer, *args):
    '''
    Asynchronous function to use our non-asynchronous style_transfer function
    '''
    await loop.run_in_executor(None, style_transfer, *args)


@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer_photo(start_image, caption=MESSAGES['start'])


@dp.message_handler(state='*', commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply(MESSAGES['help'])


@dp.message_handler(state='*', commands=['set_style'])
async def set_style_transfer(message: types.Message):
    '''
    After receiving command "set_style" the bot turns to style state
    and wait for a style image from user
    '''
    await STStates.style.set()
    await message.reply(MESSAGES['style'])


@dp.message_handler(content_types=types.ContentType.PHOTO, state=STStates.style)
async def set_style_image(message: types.Message):
    '''
    If in style state, after receiving an image the bot saves it using image's id
    and goes into content state
    '''
    style_name = 'style_{}.jpg'.format(message.from_user.id)
    await bot.download_file_by_id(message.photo[-1].file_id, style_name)
    await STStates.next()
    await bot.send_message(message.chat.id, MESSAGES['content'])


@dp.message_handler(content_types=types.ContentType.PHOTO, state=STStates.content)
async def img_style_transfer(message: types.Message):
    '''
    If in content state, after receiving an image the bot saves new image
    and performs style transfer using previously saved style image
    '''
    print(message.photo[-1].file_id)
    content_name = 'content_{}.jpg'.format(message.from_user.id)
    await bot.download_file_by_id(message.photo[-1].file_id, content_name)

    style_path = 'style_{}.jpg'.format(message.from_user.id)
    content_path = content_name

    # style transfer requires some time, so let's warn the user
    bot_msg = await bot.send_message(message.from_user.id, MESSAGES['processing'])

    output_name = 'output_{}.jpg'.format(message.from_user.id)
    # perform style transfer
    await async_st(loop, style_transfer_func, style_path, content_path, output_name)
    # delete warning message
    await bot.delete_message(message.from_user.id, bot_msg.message_id)

    output = types.InputFile(output_name)

    # send the output image to the user
    await message.answer_photo(output)

    # delete content and output files, but not the style
    os.remove(content_name)
    os.remove(output_name)


@dp.message_handler(content_types=types.ContentType.ANY, state=STStates.style)
async def not_supported_style(message: types.Message):
    '''
    If the bot receives non-images in the style state
    '''
    await bot.send_message(message.chat.id, MESSAGES['not_supported_style'])


@dp.message_handler(content_types=types.ContentType.ANY, state=STStates.content)
async def not_supported_content(message: types.Message):
    '''
    If the bot receives non-images in the content state
    '''
    await bot.send_message(message.chat.id, MESSAGES['not_supported_content'])


@dp.message_handler(content_types=types.ContentType.ANY, state=None)
async def unknown_message(message: types.Message):
    '''
    If the bot receives any type of message other then commands
    when not in particular state
    '''
    await bot.send_message(message.chat.id, MESSAGES['unknown'])


def start_bot():
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
