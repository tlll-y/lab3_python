from dataclasses import dataclass

from src.mediateka.errors import InvalidMediaItemError


@dataclass(frozen=True)
class MediaItem:
    """Представляет медиаматериал в каталоге"""

    item_id: str
    name: str
    category: str
    year: int
    creator: str
    duration_minutes: int

    def __post_init__(self) -> None:
        """Проверяет корректность полей медиаматериала"""
        if type(self.item_id) is not str:
            raise InvalidMediaItemError("Id должен быть строкой")
        if not self.item_id.strip():
            raise InvalidMediaItemError("Id не может быть пустой строкой")

        if type(self.name) is not str:
            raise InvalidMediaItemError("Название должно быть строкой")
        if not self.name.strip():
            raise InvalidMediaItemError("Название не может быть пустой строкой")

        if type(self.category) is not str:
            raise InvalidMediaItemError("Категория должна быть строкой")
        if not self.category.strip():
            raise InvalidMediaItemError("Категория не может быть пустой строкой")

        if type(self.year) is not int:
            raise InvalidMediaItemError("Год должен быть целым числом")
        if self.year <= 0:
            raise InvalidMediaItemError("Год должен быть положительным")

        if type(self.creator) is not str:
            raise InvalidMediaItemError("Имя автора должно быть строкой")
        if not self.creator.strip():
            raise InvalidMediaItemError("Имя автора не может быть пустым")

        if type(self.duration_minutes) is not int:
            raise InvalidMediaItemError("Длительность должна быть целым числом")
        if self.duration_minutes <= 0:
            raise InvalidMediaItemError("Длительность должна быть больше 0")
