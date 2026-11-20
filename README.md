# Лабораторная работа №3. Каталог объектов

## Медиатека на Python

## Описание

В лабораторной работе я сделала каталог медиаматериалов. В нём можно хранить фильмы, музыку и другие записи, находить их по названию или категории, добавлять и удалять по ID. Каталог можно сохранить в JSON и потом загрузить обратно.

Программа разделена на два основных класса: `MediaItem` описывает один медиаматериал, а `MediaCatalog` отвечает за хранение и работу со всеми объектами.

## Требования и установка

Нужен **Python 3.12 или новее**. Для самой программы сторонние библиотеки не требуются. Для тестов и проверки кода используются `pytest`, `ruff`, `mypy` и `pre-commit`.

### macOS / Linux

```bash
git clone https://github.com/tlll-y/lab3_python.git
cd lab3_python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest ruff mypy pre-commit
```

### Windows (PowerShell)

```powershell
git clone https://github.com/tlll-y/lab3_python.git
cd lab3_python
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pytest ruff mypy pre-commit
```

В `cmd` окружение активируется командой `.venv\Scripts\activate.bat`.

## Запуск

Все команды выполняются из корня проекта:

```bash
python -m src.mediateka
```

Пример вывода:

```text
Содержимое каталога:
001: Гарри Поттер (2001)
Каталог сохранён в catalog.json
Количество после загрузки: 1
```

В `main.py` для примера создаётся фильм, добавляется в каталог, затем каталог сохраняется и загружается в новый объект. Файл `catalog.json` создаётся рядом с проектом и не добавляется в Git.

## Класс `MediaItem`

Один медиаматериал содержит шесть полей:

| Поле | Тип | Что хранит |
|---|---|---|
| `item_id` | `str` | Уникальный ID |
| `name` | `str` | Название |
| `category` | `str` | Категория, например `фильм` |
| `year` | `int` | Год выпуска |
| `creator` | `str` | Автор или создатель |
| `duration_minutes` | `int` | Длительность в минутах |

Класс сделан через `@dataclass(frozen=True)`: после создания поля нельзя менять обычным присваиванием. В `__post_init__()` проверяются типы и значения. Строки не могут быть пустыми или состоять только из пробелов, а год и длительность должны быть положительными целыми числами. При неправильных данных возникает `InvalidMediaItemError`.

## Класс `MediaCatalog`

Внутри каталога используется словарь `self._items`, где ключ — ID, а значение — объект `MediaItem`

| Метод | Что делает |
|---|---|
| `add(item)` | Добавляет запись, если ID ещё не занят |
| `get(item_id)` | Возвращает запись по ID |
| `remove(item_id)` | Удаляет запись по ID |
| `find_by_category(category)` | Ищет записи с точно такой же категорией |
| `find_by_name(search)` | Ищет часть названия без учёта регистра |
| `len(catalog)` | Показывает количество записей |
| `item_id in catalog` | Проверяет наличие ID |
| `for item in catalog` | Перебирает записи в порядке добавления |
| `save(file_path)` | Сохраняет каталог в JSON |
| `load(file_path)` | Загружает каталог из JSON |



Пример работы с классами:

```python
from src.mediateka.media_catalog import MediaCatalog
from src.mediateka.media_item import MediaItem

catalog = MediaCatalog()
film = MediaItem("001", "Гарри Поттер", "фильм", 2001, "Крис Коламбус", 152)

catalog.add(film)
print(catalog.get("001").name)          # Гарри Поттер
print(catalog.find_by_name("ПОТТ"))     # Список с фильмом
print("001" in catalog)                # True
print(len(catalog))                    # 1

catalog.save("catalog.json")
```

## Сохранение и загрузка JSON

При сохранении `save()` превращает объекты в словари через `asdict()` и записывает их с помощью `json.dump()`.

Пример файла:

```json
{
    "format_version": 1,
    "items": [
        {
            "item_id": "001",
            "name": "Гарри Поттер",
            "category": "фильм",
            "year": 2001,
            "creator": "Крис Коламбус",
            "duration_minutes": 152
        }
    ]
}
```

Метод `load()` сначала читает JSON и проверяет версию, наличие списка `items` и данные каждой записи. Для этого все объекты сначала собираются в **новый временный словарь**. Только когда проверка полностью закончилась, этот словарь заменяет старый каталог.

Так обеспечивается **атомарная загрузка**: если в файле найдётся ошибка, старые данные не потеряются, а часть новых записей не попадёт в каталог.

## Обработка ошибок

Для ошибок каталога создан базовый класс `CatalogError` и его наследники:

| Исключение | Когда возникает |
|---|---|
| `InvalidMediaItemError` | Неправильные поля медиаматериала |
| `DuplicateIDError` | Попытка добавить уже существующий ID |
| `ItemNotFoundError` | Получение или удаление отсутствующего ID |
| `UnsupportedFormatVersionError` | Версия JSON не поддерживается |
| `CorruptedCatalogError` | Повреждённый JSON, неправильные поля или повторяющиеся ID при загрузке |

При ошибке загрузки, например из-за отрицательной длительности или отсутствия обязательного поля, вызывается `CorruptedCatalogError`. 

## Структура проекта

```text
lab3_python/
├── src/
│   ├── __init__.py
│   └── mediateka/
│       ├── __init__.py
│       ├── __main__.py
│       ├── constants.py
│       ├── errors.py
│       ├── main.py
│       ├── media_catalog.py
│       └── media_item.py
├── tests/
│   ├── __init__.py
│   ├── test_media_catalog.py
│   └── test_media_item.py
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
└── README.md
```

- `media_item.py` — описание и проверка одного объекта.
- `media_catalog.py` — методы каталога и работа с JSON.
- `errors.py` — собственные исключения.
- `constants.py` — версия формата JSON.
- `main.py` и `__main__.py` — пример работы и запуск пакета.
- `tests/` — тесты модели и каталога.
- `pyproject.toml` — настройки проекта, Ruff, mypy и pytest.

## Тестирование

Написан **21 тест**: 4 для `MediaItem` и 17 для `MediaCatalog`. Они проверяют создание объектов, ошибки в полях, добавление и удаление, дубликаты ID, поиск, порядок перебора, сохранение и загрузку JSON. Отдельно проверяется, что при ошибке загрузки исходный каталог остаётся без изменений.

Запуск тестов:

```bash
python -m pytest -v
```

Проверки качества кода:

```bash
python -m ruff check src tests
python -m ruff format --check src tests
python -m mypy src tests
```

Для автоматической проверки перед коммитом используется `pre-commit`:

```bash
pre-commit install
pre-commit run --all-files
```
## Итог

В лабораторной работе реализован каталог медиаматериалов на Python с отдельной моделью `MediaItem`, проверкой инвариантов, словарным хранением по ID и основными операциями добавления, получения, удаления и поиска. Перебор реализован в порядке добавления объектов.

Каталог сохраняется в JSON и восстанавливается из него. Версия структуры файла хранится в `format_version`, а при ошибке загрузки исходное содержимое каталога не изменяется благодаря временному словарю.

Работа покрыта автоматическими тестами и проверками Ruff, mypy и pre-commit