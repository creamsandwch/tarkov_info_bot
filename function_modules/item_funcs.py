from dateutil import parser as dt_parser
from datetime import datetime, timezone

from function_modules import exceptions
from function_modules.base_funcs import run_query, timedelta_formatter
from bot_settings import settings


def sell_price_finder(item: dict) -> str:
    """Находит лучшую цену на продажу предмета
    по стандартизированному запросу к API."""

    sell_for_list: list = item.get('sellFor')

    best_sell_price = 0

    for sellfor_obj in sell_for_list:
        sell_name = (sellfor_obj.get('vendor')).get('name')
        sell_price = sellfor_obj.get('price')
        sell_currency = sellfor_obj.get('currency')

        if sell_price >= best_sell_price:
            best_sell_name = sell_name
            best_sell_price = sell_price
            best_sell_currency = sell_currency

    return (
        f'Продать:\n'
        f'{best_sell_name} за '
        f"{'{0:,}'.format(best_sell_price).replace(',', ' ')} "
        f"{best_sell_currency}.\n\n"
    )


def buy_price_finder(item: dict) -> str:
    """Находит лучшую цену на покупку предмета
    по стандартизированному запросу к API."""

    buyfor_list: list = item.get('buyFor')

    if buyfor_list == []:
        return 'Данный предмет нельзя купить.'

    best_buy_price = buyfor_list[0].get('price')

    for buyfor_obj in buyfor_list:
        buy_name = ((buyfor_obj).get('vendor')).get('name')
        buy_price = buyfor_obj.get('price')
        buyfor_currency = buyfor_obj.get('currency')

        if buy_price <= best_buy_price:
            best_buy_name = buy_name
            best_buy_price = buy_price
            best_buy_currency = buyfor_currency

    return (
        f'Купить:\n'
        f"{best_buy_name} за "
        f"{'{0:,}'.format(best_buy_price).replace(',', ' ')} "
        f"{best_buy_currency}.\n\n"
    )


def get_item_avgprice_by_name(
    item_name: str,
    language: str = settings.QUERY_LANG
) -> str:
    """Возвращает сообщение о цене предмета,
    либо о результатах неудачного поиска по имени."""

    query = (
        """query {{
            items(name: "{0}", lang: {1}) {{
                name
                updated
                avg24hPrice
                sellFor {{
                    vendor {{
                        name
                    }}
                    price
                    currency
                }}
                buyFor {{
                    vendor {{
                        name
                    }}
                price
                currency
                }}
            }}
        }}""".format(item_name, language)
    )

    response = run_query(query)

    try:
        data = response.get('data')
        items = data.get('items')
        if items == []:
            raise exceptions.NoItemFound
        elif len(items) > 1:
            raise exceptions.MoreThatOneItemFound

        item = items[0]
        found_name = item.get('name')

        best_prices_output: str = (
            sell_price_finder(item) + buy_price_finder(item)
        )

        updated = item.get('updated')
        updated_dt_parsed = dt_parser.parse(updated)

        updated = (
            datetime.now().astimezone(timezone.utc)
            - updated_dt_parsed.astimezone(timezone.utc)
        )
        hours, minutes = map(int, timedelta_formatter(updated))
    except KeyError:
        return (response['errors']).message
    except exceptions.NoItemFound:
        return f'Не найдено ни одного предмета по запросу {item_name}.'

    return (
        f'{found_name}.\n\n'
        f'{best_prices_output}'
        f'Обновлено {hours}ч {minutes}м назад.'
    )


def get_eft_service_status():
    """Возвращает ответ от API в виде списка со словарями
    статусов сервисов EFT."""

    query = (
        """query {
            status {
                currentStatuses {
                    name
                    message
                    status
                    statusCode
                }
            }
        }"""
    )

    response = run_query(query)

    try:
        data = response.get('data')
        status = data.get('status')
        current_statuses = status.get('currentStatuses')
    except KeyError:
        return response['errors'].message

    return current_statuses


if __name__ == '__main__':
    pass
