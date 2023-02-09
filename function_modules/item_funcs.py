from dateutil import parser as dt_parser
from datetime import datetime, timezone

from function_modules.example import run_query, timedelta_formatter
from bot_settings.settings import QUERY_LANG


def get_item_avgprice_by_name(item_name: str) -> str:
    query = """
    query {{
        items(name: "{0}", lang: {1}) {{
            name
            updated
            avg24hPrice
        }}
    }}
    """.format(item_name, QUERY_LANG)

    response = run_query(query)

    try:
        data = response.get('data')
        items_list = data.get('items')
        item_fields = items_list[0]

        updated = item_fields.get('updated')
        updated_dt_parsed = dt_parser.parse(updated)

        updated = (
            datetime.now().astimezone(timezone.utc)
            - updated_dt_parsed.astimezone(timezone.utc)
        )
        hours, minutes = map(int, timedelta_formatter(updated))

        avg24hprice = item_fields.get('avg24hPrice')

        if avg24hprice == 0:
            return (
                f"{item_name} не продается на барахолке."
            )
    except KeyError:
        return (response['errors']).message

    return (
        f'{str.capitalize(item_name)} стоит {avg24hprice}р. '
        f'Обновлено {hours}ч {minutes}м назад.'
    )


def main():
    pass


if __name__ == '__main__':
    pass
