import os


start_image = 'AgACAgIAAxkBAAN5Yeu3Cg67Vs3D1b1HpCqcrfz0fU8AAue5MRvYwmBLRO6y1jaLRhkBAAMCAAN4AAMjBA'

# webhook settings
BOT_TOKEN = os.getenv('TOKEN')
WEBHOOK_HOST = 'https://dls-nst-bot.herokuapp.com/'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 3001))