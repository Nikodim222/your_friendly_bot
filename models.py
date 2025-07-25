"""
* Внутренние типы данных и константы в рамках проекта
* *************************
* В данном файле хранятся внутренние типы данных и константы,
* которые созданы для нужд работы проекта.
*
* @author Ефремов А. В., 22.07.2025
"""

from enum import Enum

class Constant(Enum):
    GLOBAL_CODEPAGE = "cp1251" # кодировка Windows-1251 в текстовых файлах
    SETTINGS_FILE = "settings.ini"  # путь к файлу конфигурации
