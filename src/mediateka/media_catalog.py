import json
from collections.abc import Iterator
from dataclasses import asdict

from src.mediateka.constants import FORMAT_VERSION
from src.mediateka.errors import (
    CorruptedCatalogError,
    DuplicateIDError,
    InvalidMediaItemError,
    ItemNotFoundError,
    UnsupportedFormatVersionError,
)
from src.mediateka.media_item import MediaItem


class MediaCatalog:
    """Хранит медиаматериалы и предоставляет методы работы с ними"""

    def __init__(self) -> None:
        """Создаёт пустой каталог медиаматериалов"""
        self._items: dict[str, MediaItem] = {}

    def add(self, item: MediaItem) -> None:
        """Добавляет медиаматериал в каталог"""

        if item.item_id in self._items:
            raise DuplicateIDError("Объект с таким ID уже существует")

        self._items[item.item_id] = item

    def get(self, item_id: str) -> MediaItem:
        """Возвращает медиаматериал по его идентификатору"""
        if item_id not in self._items:
            raise ItemNotFoundError("Медиаматериал не найден")

        return self._items[item_id]

    def remove(self, item_id: str) -> None:
        """Удаляет медиаматериал из каталога по ID"""
        if item_id not in self._items:
            raise ItemNotFoundError("Медиаматериал не найден")

        del self._items[item_id]

    def find_by_category(self, category: str) -> list[MediaItem]:
        """Возвращает медиаматериалы указанной категории"""
        result: list[MediaItem] = []

        for item in self._items.values():
            if item.category == category:
                result.append(item)

        return result

    def find_by_name(self, search: str) -> list[MediaItem]:
        """Поиск медиаматериалов по части названия без учёта регистра"""
        result: list[MediaItem] = []

        for item in self._items.values():
            if search.casefold() in item.name.casefold():
                result.append(item)

        return result

    def __len__(self) -> int:
        """Возвращает количество медиаматериалов в каталоге"""

        return len(self._items)

    def __contains__(self, item_id: str) -> bool:
        """Проверяет наличие медиаматерила по ID"""

        return item_id in self._items

    def __iter__(self) -> Iterator[MediaItem]:
        """Позволяет перебирать медиаматериалы в порядке добавления"""

        return iter(self._items.values())

    def save(self, file_path: str) -> None:
        """Сохраняет каталог медиаматериалов в JSON-файл"""
        items_data = []

        for item in self._items.values():
            items_data.append(asdict(item))

        data = {
            "format_version": FORMAT_VERSION,
            "items": items_data,
        }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load(self, file_path: str) -> None:
        """Загружает медиаматериалы из JSON-файла"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as err:
            raise CorruptedCatalogError("Неправильный формат JSON") from err
        if not isinstance(data, dict):
            raise CorruptedCatalogError("Корень JSON должен быть словарём")
        if "format_version" not in data:
            raise CorruptedCatalogError("В JSON отсутствует версия формата")
        if type(data["format_version"]) is not int:
            raise CorruptedCatalogError("Версия формата должна быть целым числом")
        if data["format_version"] != FORMAT_VERSION:
            raise UnsupportedFormatVersionError("Неподдерживаемая версия JSON")

        if "items" not in data:
            raise CorruptedCatalogError("В JSON отсутствует список медиаматериалов")

        if not isinstance(data["items"], list):
            raise CorruptedCatalogError("Поле items должно быть списком")

        new_items: dict[str, MediaItem] = {}
        for item_data in data["items"]:
            if not isinstance(item_data, dict):
                raise CorruptedCatalogError("Медиаматериал должен быть словарём")

            try:
                item = MediaItem(**item_data)
            except (TypeError, InvalidMediaItemError) as err:
                raise CorruptedCatalogError(
                    "Некорректные данные медиаматериала"
                ) from err

            if item.item_id in new_items:
                raise CorruptedCatalogError("Повторяющийся ID в JSON")

            new_items[item.item_id] = item

        self._items = new_items
