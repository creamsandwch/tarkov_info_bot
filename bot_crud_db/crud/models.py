import typing

from django.db import models

from .hideout_models.items_models import Item
from .hideout_models import exceptions


class HideoutStation():
    level: int
    running: bool
    interactive: bool
    cells: list
    allowed_items: typing.Set[Item, ]

    def __init__(
            self,
            level=0,
            running=False,
            interactive=False,
            cells=None,
            allowed_items=None
    ) -> None:
        self.level = level
        self.running = running
        self.interactive = interactive
        self.cells = cells
        self.allowed_items = allowed_items

    @property
    def running(self):
        return self.running

    @running.setter
    def running(self, value):
        if self.level < 1 and value is True:
            raise Exception('Модуль не построен!')
        self._running = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if not 0 <= value <= 3:
            raise Exception('Уровень должен быть 0, 1, 2 или 3.')
        self._level = value

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value: int):
        if not self.interactive:
            raise Exception(
                'Неинтерактивная станция не имеет ячеек.'
            )
        if type(value) != int or value == 0:
            raise Exception(
                'Некорректно передано количество ячеек (not int or 0).'
            )
        self._cells = [None] * value

    def fill_cell(self, cell_index: int, item: Item):
        """Ставит на незанятую ячейку станции подходящий предмет
        с ресурсом и присваивает ему статус 'установлен'."""

        if item not in self.allowed_items:
            raise exceptions.ItemNotSupportedByStation

        if self.cells[cell_index] is not None:
            raise exceptions.CellIsFilledOrEmpty('Ячейка занята.')

        self.cells[cell_index] = item
        item.installed = True

    def unfill_cell(self, cell_index: int):
        """Освобождает занятую ячейку станции и снимает у предмета
        статус 'установлен'."""

        if self.cells[cell_index] is None:
            raise exceptions.CellIsFilledOrEmpty('Ячейка пуста.')

        item = self.cells[cell_index]
        self.cells[cell_index] = None
        return item


# This should be inherited from "models.Model" later,
# it is not inherited now for testing purposes.
class Hideout:
    owner = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    air_filtrator = HideoutStation(
        level=0, running=False, interactive=True, cells=3
    )


if __name__ == '__main__':
    hideout = Hideout()
    print(hideout.air_filtrator.cells)
