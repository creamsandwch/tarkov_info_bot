import os
import logging
import sys

import telegram
from dotenv import load_dotenv


log_format = (
    '%(asctime)s, %(levelname)s, %(funcName)s, '
    '%(lineno)d, %(message)s, %(name)s')
formatter = logging.Formatter(
    fmt=log_format,
)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.INFO)

file_logger = logging.FileHandler('logs.log')
file_logger.setLevel(logging.DEBUG)

logging.basicConfig(
    handlers=(console_logger, file_logger),
    format=log_format,
    level=logging.DEBUG,
)


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def check_tokens(bot: telegram.Bot, message: str):
    '''Проверяет доступность токенов.'''
    return all(BOT_TOKEN, ADMIN_CHAT_ID)


def send_message_to_admin(bot: telegram.Bot, message: str, chat_id: str):
    """Отправляет сообщение от бота в чат админа."""
    try:
        bot.send_message(chat_id=chat_id, text=message)
        logging.debug('Бот отправил сообщение.')
    except Exception as error:
        logging.error(f'{error}: ошибка при отправке сообщения ботом.')


def main():
    """Основная логика."""
    if check_tokens():
        logging.info('Все токены доступны')
    else:
        logging.critical('Один или несколько токенов недоступны')
        sys.exit()

    bot = telegram.Bot(token=BOT_TOKEN)
    send_message_to_admin(
        bot=bot,
        message='Все токены доступны.',
        chat_id=ADMIN_CHAT_ID,
    )


if __name__ == '__main__':
    main()
