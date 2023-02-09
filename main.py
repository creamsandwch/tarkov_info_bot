import os
import logging
import sys

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

from function_modules import item_funcs


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


def check_tokens():
    '''Проверяет доступность токенов.'''
    return all([BOT_TOKEN, ADMIN_CHAT_ID])


def standard_response(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Используйте команду /p <название предмета> для получения цены.'
    )


def send_msg(bot: telegram.Bot, message: str, chat_id: str = ADMIN_CHAT_ID):
    """Отправляет сообщение от бота. Отправляет в чат админу - по умолчанию."""
    try:
        bot.send_message(chat_id=chat_id, text=message)
        logging.debug('Бот отправил сообщение.')
    except Exception as error:
        logging.error(f'{error}: ошибка при отправке сообщения ботом.')


def send_item_price(update, context):
    """Команда запроса цены предмета по его имени."""
    chat = update.effective_chat
    try:
        item_name = ' '.join(context.args)
        item_price_response = item_funcs.get_item_avgprice_by_name(item_name)
        context.bot.send_message(chat_id=chat.id, text=item_price_response)
    except (IndexError, ValueError):
        context.bot.send_message('There is no item name to search for.')


def main():
    """Основная логика."""
    if check_tokens():
        logging.info('Все токены доступны')
    else:
        logging.critical('Один или несколько токенов недоступны')
        sys.exit()

    updater = Updater(token=BOT_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('p', send_item_price))
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.text, standard_response
        )
    )
    updater.start_polling()


if __name__ == '__main__':
    main()
