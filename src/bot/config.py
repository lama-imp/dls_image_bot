import os


start_image = 'AgACAgIAAxkBAAN5Yeu3Cg67Vs3D1b1HpCqcrfz0fU8AAue5MRvYwmBLRO6y1jaLRhkBAAMCAAN4AAMjBA'

# webhook settings
BOT_TOKEN = os.getenv('TOKEN')
WEBHOOK_HOST = 'https://dls-nst-bot.herokuapp.com/'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT'))