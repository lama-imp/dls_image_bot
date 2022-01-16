import logging

from aiogram import Bot, Dispatcher, executor, types

from src.model.StyleTransfer import StyleTransfer

with open('token.txt') as f:
    API_TOKEN = f.readline().strip()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=types.ContentType.ANY)
async def echo(message: types.Message):
    print(message.photo[-1].file_id)
    content_name = 'content_{}.jpg'.format(message.from_user.id)
    a = await bot.download_file_by_id(message.photo[-1].file_id, content_name)

    style_path = 'style2.jpg'
    content_path = content_name

    s_transfer = StyleTransfer(style_path, content_path)
    s_transfer.run_style_transfer()
    s_transfer.save_image('output_{}.jpg'.format(message.from_user.id))
    output = types.InputFile('output_{}.jpg'.format(message.from_user.id))

    await message.answer_photo(output)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)