from dataclasses import FrozenInstanceError

import pytest

from src.mediateka.errors import InvalidMediaItemError
from src.mediateka.media_item import MediaItem


def test_create_valid_media_item() -> None:
    """Проверяет создание медиаматериала с корректными данными"""

    item = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    assert item.item_id == "001"
    assert item.name == "Гарри Поттер"
    assert item.year == 2001


def test_invalid_duration() -> None:
    """Проверяет ошибку при отрицательной длительности"""
    with pytest.raises(InvalidMediaItemError):
        MediaItem(
            item_id="001",
            name="Гарри Поттер",
            category="фильм",
            year=2001,
            creator="Крис Коламбус",
            duration_minutes=-152,
        )


def test_empty_name() -> None:
    """Проверяет ошибку при пустом названии."""
    with pytest.raises(InvalidMediaItemError):
        MediaItem(
            item_id="001",
            name="",
            category="фильм",
            year=2001,
            creator="Крис Коламбус",
            duration_minutes=152,
        )


def test_media_item_is_frozen() -> None:
    """Проверяет запрет изменения полей медиаматериала"""
    item = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    field_name = "year"

    with pytest.raises(FrozenInstanceError):
        setattr(item, field_name, -100)
