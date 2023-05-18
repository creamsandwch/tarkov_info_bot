class ItemNotSupportedByStation(Exception):
    """Станция не поддерживает этот предмет."""
    pass


class CellIsFilledOrEmpty(Exception):
    """Некорректное обращение к ячейке"""
    pass
