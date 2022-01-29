import os


BOT_TOKEN = os.getenv('TOKEN')
start_image = 'AgACAgIAAxkBAAN5Yeu3Cg67Vs3D1b1HpCqcrfz0fU8AAue5MRvYwmBLRO6y1jaLRhkBAAMCAAN4AAMjBA'
WEBHOOK_HOST = 'http://195.234.208.114/'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 3001))