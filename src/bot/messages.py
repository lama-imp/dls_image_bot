'''
Text of messages to be send to user
'''


start_message = '''Приветствую! Я умею переносить стиль с одного изображения на другое, как на картинке выше.
Чтобы начать, отправьте команду /set_style
Если что-то непонятно, отправьте команду /help'''
help_message = '''Сначала нужно отправить команду /set_style и выбрать изображение, стиль с которого вы хотите перенести.
Затем можно отправлять другие изображения, на которые будет перенесён этот стиль.
Если хотите изменить стиль, снова отправьте команду /set_style и отправьте новое изображение'''
style_message = '''Отправьте изображение, с которого хотите перенести стиль'''
content_message = '''Теперь отправьте изображение, на которое хотите перенести стиль'''
not_supported_style_message = '''Я могу работать только с изображениями.
Отправьте изображение, с которого хотите перенести стиль'''
not_supported_content_message = '''Я могу работать только с изображениями.
Отправьте изображение, на которое хотите перенести стиль'''
unknown_message = '''Не понимаю.\nОтправьте команду /help, чтобы посмотреть объяснение моей работы'''
processing_message = '''Выполняю, обработка изображения занимает примерно 10 минут...'''


MESSAGES = {
    'start': start_message,
    'help': help_message,
    'style': style_message,
    'content': content_message,
    'not_supported_style': not_supported_style_message,
    'not_supported_content': not_supported_content_message,
    'unknown': unknown_message,
    'processing': processing_message,
}