class CatalogError(Exception):
    """Базовое  исключение для ошибок каталога"""


class InvalidMediaItemError(CatalogError):
    """Ошибка при создании некорректного медиа"""


class DuplicateIDError(CatalogError):
    """Ошибка при добавлении объекта с существующим ID"""


class ItemNotFoundError(CatalogError):
    """Ошибка при обращении к отсутствующему медиаматериалу"""


class UnsupportedFormatVersionError(CatalogError):
    """Ошибка при использовании неподдерживаемой версии JSON"""


class CorruptedCatalogError(CatalogError):
    """Ошибка при повреждении структуры или данных JSON-файла"""
