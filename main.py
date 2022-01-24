from aiogram import executor

from src.bot.bot import dp, on_startup


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        skip_updates=True,
        host="0.0.0.0",
        port=3001,
    )
