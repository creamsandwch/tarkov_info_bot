class NoItemFound(Exception):
    """Вызывается, когда список найденных предметов пуст."""

    pass


class MoreThatOneItemFound(Exception):
    """Вызывается, когда найдено больше одного предмета."""

    pass
