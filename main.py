from dateutil import parser as dt_parser
from datetime import datetime, timezone

from example import run_query, timedelta_formatter


def get_item_avgprice_by_name(item_name):
    query = """
    query {{
        items(name: "{0}") {{
            name
            updated
            avg24hPrice
        }}
    }}
    """.format(item_name)
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
        hours, minutes = timedelta_formatter(updated)

        avg24hprice = item_fields.get('avg24hPrice')
    except KeyError:
        return (response['errors']).message
    return (
        f'{item_name} price is {avg24hprice}. '
        f'Updated {hours}h, {minutes}m ago.'
    )


name = input('Введите название предмета: ')

print(get_item_avgprice_by_name(name))
