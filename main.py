import os
import logging
import sys

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

from function_modules import item_funcs
from function_modules import exceptions


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
    """Справка по командам, выдаваемая на любое текстовое сообщение."""

    chat = update.effective_chat

    info_message = (
            '/p <название предмета> - средняя цена на барахолке.\n'
            '/status - состояние сервисов EFT.\n'
        )
    context.bot.send_message(
        chat_id=chat.id,
        text=info_message
    )


def send_item_price(update, context):
    """Обработчик команды запроса цены предмета по его имени."""
    chat = update.effective_chat
    try:
        context.args[0]

        item_name = ' '.join(context.args)

        item_price_response = item_funcs.get_item_avgprice_by_name(
            item_name,
        )
        context.bot.send_message(chat_id=chat.id, text=item_price_response)
        logging.info('Бот отправил сообщение с ценой о предмете.')
    except IndexError as error:
        context.bot.send_message(
            chat_id=chat.id,
            text='Команде не предоставлено имя предмета.'
        )
        logging.info(
            'Команде /p не был передан аргумент.'
            f'Error: {error}'
        )
    except exceptions.NoItemFound as error:
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Не найдено предметов по имени {item_name}'
        )
        logging.info(
            f'Не найдено ни одного предмета по запросу {item_name}. '
            f'Error: {error}'
        )
    except exceptions.MoreThatOneItemFound as error:
        context.bot.send_message(
            chat_id=chat.id,
            text='Найдено более одного предмета. Уточните запрос.'
        )
        logging.info(
            f'Найдено более одного предмета по имени {item_name}.'
            f'Error: {error}'
        )


def send_eft_service_status(update, context):
    """Обработчик команды запроса статусов сервисов EFT."""
    chat = update.effective_chat

    statuses = item_funcs.get_eft_service_status()
    message_text = ''

    try:
        for status in statuses:
            message_not_null_flag = 1
            if status.get("message") is None:
                message_not_null_flag = 0

            message_text += (
                f'{status.get("name")}: ' +
                f'{status.get("statusCode")}.' +
                (not message_not_null_flag) * '\n' +
                message_not_null_flag * f' {str(status.get("message"))}\n'
            )
        context.bot.send_message(chat_id=chat.id, text=message_text)
        logging.info('Бот отправил сообщение о статусах сервисов EFT.')
    except (IndexError, ValueError):
        context.bot.send_message(
            chat_id=chat.id,
            text='Информация о статусах EFT недоступна.'
        )
        logging.warning(
            'Бот не смог получить корректный ответ от API со статусами EFT.'
        )


def main():
    """Основная логика."""
    if check_tokens():
        logging.info('Все токены доступны')
    else:
        logging.critical('Один или несколько токенов недоступны')
        sys.exit()

    updater = Updater(token=BOT_TOKEN, use_context=True)

    updater.dispatcher.add_handler(
        CommandHandler(command='p', callback=send_item_price, pass_args=True))
    updater.dispatcher.add_handler(
        CommandHandler('status', send_eft_service_status)
    )

    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, standard_response)
    )

    updater.start_polling(poll_interval=10)
    updater.idle()


if __name__ == '__main__':
    main()
