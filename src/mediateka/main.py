from src.mediateka.media_catalog import MediaCatalog
from src.mediateka.media_item import MediaItem


def main() -> None:
    """Показывает работу медиатеки"""
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

    print("Содержимое каталога:")

    for item in catalog:
        print(f"{item.item_id}: {item.name} ({item.year})")

    catalog.save("catalog.json")
    print("Каталог сохранён в catalog.json")

    new_catalog = MediaCatalog()
    new_catalog.load("catalog.json")

    print(f"Количество после загрузки: {len(new_catalog)}")


if __name__ == "__main__":
    main()
