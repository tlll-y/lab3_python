import json
from pathlib import Path

import pytest

from src.mediateka.errors import (
    CorruptedCatalogError,
    DuplicateIDError,
    ItemNotFoundError,
    UnsupportedFormatVersionError,
)
from src.mediateka.media_catalog import MediaCatalog
from src.mediateka.media_item import MediaItem


def test_add_mediaitem() -> None:
    """Проверяет добавление медиаматериала в каталог"""
    catalog = MediaCatalog()

    item = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    catalog.add(item)
    assert catalog._items["001"] == item


def test_duplicate_id() -> None:
    """Проверяет ошибку при добавлении повторяющегося ID"""
    catalog = MediaCatalog()

    item = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    catalog.add(item)
    with pytest.raises(DuplicateIDError):
        catalog.add(item)


def test_get_existing_item() -> None:
    """Проверяет получение медиаматериала по ID"""
    catalog = MediaCatalog()

    item = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    catalog.add(item)
    result = catalog.get("001")
    assert result == item
    assert result.name == "Гарри Поттер"


def test_get_missing_item() -> None:
    """Проверяет ошибку при поиске отсутствующего медиаматериала"""
    catalog = MediaCatalog()

    with pytest.raises(ItemNotFoundError):
        catalog.get("8490392892")


def test_remove_existing_item() -> None:
    """Проверяет удаление существующего медиаматериала"""
    catalog = MediaCatalog()

    item = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    catalog.add(item)
    catalog.remove("001")
    with pytest.raises(ItemNotFoundError):
        catalog.get("001")


def test_remove_missing_item() -> None:
    """Проверяет удаление несуществующего медиаматериала"""
    catalog = MediaCatalog()

    with pytest.raises(ItemNotFoundError):
        catalog.remove("8430203578938")


def test_find_by_category() -> None:
    """Проверяет поиск медиаматериалов по категории"""
    catalog = MediaCatalog()

    film = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    music = MediaItem(
        item_id="002",
        name="SleepMode",
        category="музыка",
        year=2016,
        creator="Bones",
        duration_minutes=164,
    )

    catalog.add(film)
    catalog.add(music)
    result = catalog.find_by_category("фильм")
    assert result == [film]
    assert catalog.find_by_category("подкаст") == []


def test_find_by_name() -> None:
    """Проверяет поиск по части названия без учёта регистра"""
    catalog = MediaCatalog()

    film1 = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    film2 = MediaItem(
        item_id="002",
        name="Один дома",
        category="фильм",
        year=1990,
        creator="Крис Коламбус",
        duration_minutes=103,
    )
    catalog.add(film1)
    catalog.add(film2)

    result = catalog.find_by_name("ПОТТ")
    assert result == [film1]


def test_contains_item() -> None:
    """Проверяет наличие и отсутствие ID в каталоге"""
    catalog = MediaCatalog()

    item = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    catalog.add(item)

    assert "001" in catalog
    assert "56789098765" not in catalog


def test_iteration_order() -> None:
    """Проверяет порядок перебора медиаматериалов"""
    catalog = MediaCatalog()
    film1 = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )
    film2 = MediaItem(
        item_id="002",
        name="Один дома",
        category="фильм",
        year=1990,
        creator="Крис Коламбус",
        duration_minutes=103,
    )
    catalog.add(film1)
    catalog.add(film2)
    result = list(catalog)
    assert result == [film1, film2]


def test_save_catalog(tmp_path: Path) -> None:
    """Проверяет сохранение каталога в JSON-файл"""
    catalog = MediaCatalog()

    film = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    catalog.add(film)

    file_path = tmp_path / "catalog.json"
    catalog.save(str(file_path))
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["format_version"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Гарри Поттер"
    assert data["items"][0]["item_id"] == "001"


def test_load_catalog(tmp_path: Path) -> None:
    """Проверяет восстановление каталога из JSON-файла"""
    catalog1 = MediaCatalog()

    film = MediaItem(
        item_id="001",
        name="Гарри Поттер",
        category="фильм",
        year=2001,
        creator="Крис Коламбус",
        duration_minutes=152,
    )

    catalog1.add(film)

    file_path = tmp_path / "catalog.json"
    catalog1.save(str(file_path))

    catalog2 = MediaCatalog()
    catalog2.load(str(file_path))
    assert len(catalog2) == 1
    assert "001" in catalog2

    loaded_film = catalog2.get("001")
    assert loaded_film == film


def test_atomic_load(tmp_path: Path) -> None:
    """Проверяет сохранение старого каталога при ошибке загрузки"""
    catalog = MediaCatalog()

    old_film = MediaItem(
        item_id="001",
        name="Титаник",
        category="фильм",
        year=1997,
        creator="Джеймс Кэмерон",
        duration_minutes=194,
    )

    catalog.add(old_film)

    data = {
        "format_version": 1,
        "items": [
            {
                "item_id": "002",
                "name": "Гарри Поттер",
                "category": "фильм",
                "year": 2001,
                "creator": "Крис Коламбус",
                "duration_minutes": 152,
            },
            {
                "item_id": "003",
                "name": "Один дома",
                "category": "фильм",
                "year": 1990,
                "creator": "Крис Коламбус",
                "duration_minutes": -103,
            },
        ],
    }

    file_path = tmp_path / "broken_catalog.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

    with pytest.raises(CorruptedCatalogError):
        catalog.load(str(file_path))

    assert len(catalog) == 1
    assert catalog.get("001") == old_film
    assert "002" not in catalog
    assert "003" not in catalog


def test_corrupted_json(tmp_path: Path) -> None:
    """Проверяет ошибку при повреждённом JSON"""
    catalog = MediaCatalog()

    file_path = tmp_path / "broken.json"
    file_path.write_text('{"format_version": 1,', encoding="utf-8")

    with pytest.raises(CorruptedCatalogError):
        catalog.load(str(file_path))


def test_unsupported_format_version(tmp_path: Path) -> None:
    """Проверяет ошибку при неподдерживаемой версии JSON"""
    catalog = MediaCatalog()

    file_path = tmp_path / "version.json"
    file_path.write_text(
        '{"format_version": 2, "items": []}',
        encoding="utf-8",
    )

    with pytest.raises(UnsupportedFormatVersionError):
        catalog.load(str(file_path))


def test_duplicate_id_in_json(tmp_path: Path) -> None:
    """Проверяет ошибку при повторяющихся ID в JSON"""
    catalog = MediaCatalog()

    film_data = {
        "item_id": "001",
        "name": "Гарри Поттер",
        "category": "фильм",
        "year": 2001,
        "creator": "Крис Коламбус",
        "duration_minutes": 152,
    }

    data = {
        "format_version": 1,
        "items": [film_data, film_data],
    }

    file_path = tmp_path / "duplicate.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

    with pytest.raises(CorruptedCatalogError):
        catalog.load(str(file_path))

    assert len(catalog) == 0


def test_missing_field_in_json(tmp_path: Path) -> None:
    """Проверяет ошибку при отсутствии обязательного поля"""
    catalog = MediaCatalog()

    data = {
        "format_version": 1,
        "items": [
            {
                "item_id": "001",
                "name": "Гарри Поттер",
                "category": "фильм",
                "year": 2001,
                "duration_minutes": 152,
            }
        ],
    }

    file_path = tmp_path / "missing_field.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

    with pytest.raises(CorruptedCatalogError):
        catalog.load(str(file_path))

    assert len(catalog) == 0
