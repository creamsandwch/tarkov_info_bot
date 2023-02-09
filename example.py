import requests
import datetime


def run_query(query: str) -> str:
    """Базовая функция для запроса к GraphQL API"""
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        'https://api.tarkov.dev/graphql',
        headers=headers,
        json={'query': query}
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            "Query failed to run by returning code of {}. {}".format(
                response.status_code, query
            )
        )


def timedelta_formatter(duration: datetime.timedelta) -> str:
    """Форматирует объект timedelta в кортеж, содержащий часы и минуты."""
    seconds = duration.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return (hours, minutes)
