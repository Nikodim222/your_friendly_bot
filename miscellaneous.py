from datetime import datetime
import os, sys
import socket
import psutil, platform
import random

class Miscellaneous:

    @staticmethod
    def get_current_time() -> str:
        """
        * Получение текущей даты и времени
        *
        * @param Текущая дата и время
        """
        return datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    @staticmethod
    def print_message(msg: str) -> None:
        """
        * Вывод сообщения на экран с текущей датой и временем
        *
        * @param Текст сообщения
        """
        if not "".__eq__(msg):
            print(f"[{Miscellaneous.get_current_time()}] >> {msg}")

    @staticmethod
    def is_file_readable(filepath: str) -> bool:
        """
        * Проверка доступности файла для чтения
        *
        * @param Имя файла
        * @return True - файл доступа; False - файл недоступен
        """
        if (
            (not os.path.exists(filepath))
            or (not os.path.isfile(filepath))
            or (not os.access(filepath, os.R_OK))
        ):
            return False
        else:
            return True

    @staticmethod
    def get_local_ip_addresses():
        """
        * Список IP-адресов для сетевых интерфейсов
        *
        * @return Массив IP-адресов
        """
        ip_addresses = []
        hostname:str = socket.gethostname()
        try:
            ip_addresses = socket.gethostbyname_ex(hostname)[2] # Получаем список IP-адресов
        except socket.gaierror:
            pass
        return ip_addresses

    @staticmethod
    def get_username() -> str:
        """
        * Возвращает имя пользователя, работающего под Windows или Linux
        *
        * @return Имя пользователя
        """
        if sys.platform == "win32":
            return os.environ.get("USERNAME")
        else:
            return os.environ.get("USER")

    @staticmethod
    def get_running_processes():
        """
        * Список имён работающих процессов
        *
        * @return Массив имён работающих процессов
        """
        process_names = []
        for process in psutil.process_iter(['pid', 'name']): # Итерируемся по процессам
            try:
                process_names.append(process.info['name']) # Добавляем имя процесса в список
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass # игнорируем ошибки, если процесс исчез, или нет прав доступа
        return process_names

    @staticmethod
    def get_system_properties():
        """
        * Получение характеристик операционной системы
        *
        * @return Кортеж с характеристиками операционной системы
        """
        os_name: str = platform.system()
        os_version: str = platform.version()
        os_release: str = platform.release()
        memory = psutil.virtual_memory()
        total_memory: str = f'{memory.total / (1024**3):.2f} ГБ'
        used_memory: str = f'{memory.used / (1024**3):.2f} ГБ'
        available_memory: str = f'{memory.available / (1024**3):.2f} ГБ'
        percent_memory: str = f'{memory.percent}%'
        return os_name, os_version, os_release, total_memory, used_memory, available_memory, percent_memory

    @staticmethod
    def get_phrase_outta_file(filepath: str, codepage: str) -> str:
        """
        * Случайная строка из текстового файла
        *
        * @param Имя текстового файла
        * @param Кодировка текстового файла
        * @return Случайная строка из текстового файла
        """
        MAX_LINES_TO_READ: int = 1000  # ограничение на количество строк для чтения
        if not Miscellaneous.is_file_readable(filepath):
            return ""  # возвращаем пустую строку, если файл недоступен
        try:
            with open(filepath, "r", encoding=codepage) as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= MAX_LINES_TO_READ:
                        break
                    lines.append(line.strip())
            lines = [line for line in lines if line]  # удаляем пустые строки из списка
            if not lines:
                return ""
            random_phrase: str = random.choice(lines)  # выбираем случайную строку
            return random_phrase
        except Exception as e:
            return ""
