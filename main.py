"""
* ПО "Твой дружелюбный бот"
* *************************
* Программа является ботом для сервиса "Telegram".
* Для работы программы требуется Python 3. Предварительно
* требуется установить необходимые библиотеки:
* $ pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip
* $ pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org configparser
* $ pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org psutil
* Программа является кроссплатформенной. Она должна работать
* под Microsoft Windows, Linux, macOS и т.д.
*
* @author Ефремов А. В., 30.06.2025
"""

import os
import configparser
import argparse

from requests.exceptions import ProxyError
from telebot.apihelper import ApiTelegramException
from requests.exceptions import ReadTimeout

import telebot
from telebot import apihelper

from miscellaneous import Miscellaneous

GLOBAL_CODEPAGE: str = "cp1251" # кодировка Windows-1251 в текстовых файлах
SETTINGS_FILE: str = "settings.ini"  # путь к файлу конфигурации
MSG_NUMBER_LIMIT: int = 15 # лимит на количество одновременных сообщений от бота к пользователю
cnt: int = 0

def get_bot_config():
    """
    * Получение конфигурации для бота
    *
    * @return token, http_proxy, https_proxy
    """
    global SETTINGS_FILE
    global GLOBAL_CODEPAGE
    GLOBAL_SECTION: str = "global"
    PROXY_SECTION: str = "proxy"
    NO_PROXY: str = "DIRECT"
    TOKEN: str = "api_token"
    HTTP_PROXY: str = "http"
    HTTPS_PROXY: str = "https"
    config = configparser.ConfigParser()
    try:
        with open(SETTINGS_FILE, 'r', encoding=GLOBAL_CODEPAGE) as f:
            config.read_file(f)
            if GLOBAL_SECTION in config and TOKEN in config[GLOBAL_SECTION]:
                v_token: str = config[GLOBAL_SECTION][TOKEN].strip()
            if PROXY_SECTION in config and HTTP_PROXY in config[PROXY_SECTION]:
                v_http_proxy: str = config[PROXY_SECTION][HTTP_PROXY].strip()
                if v_http_proxy.upper() == NO_PROXY:
                    v_http_proxy = ""
            if PROXY_SECTION in config and HTTPS_PROXY in config[PROXY_SECTION]:
                v_https_proxy: str = config[PROXY_SECTION][HTTPS_PROXY].strip()
                if v_https_proxy.upper() == NO_PROXY:
                    v_https_proxy = ""
            if "".__eq__(v_token):
                return None, None, None
            else:
                return v_token, v_http_proxy, v_https_proxy
    except FileNotFoundError:
        Miscellaneous.print_message(f"Ошибка: Файл настроек не найден: {SETTINGS_FILE}")
        return None, None, None
    except Exception as e:
        Miscellaneous.print_message(f"Ошибка при чтении файла настроек: {e}")
        return None, None, None

def send_message(bot: telebot, chat_id: int, msg: str) -> None:
    """
    * Отправка сообщения для пользователя в Telegram
    *
    * @param bot Экземпляр бота
    * @param chat_id Уникальный идентификатор пользователя в Telegram
    * @param msg Текст сообщения
    """
    if not "".__eq__(msg):
        bot.send_message(chat_id, msg)
        Miscellaneous.print_message(f"Ответ пользователю {chat_id}: {chr(34)}{msg}{chr(34)}.")

def print_error(err_msg: str, err_code: str) -> None:
    """
    * Вывод сообщения об ошибке
    *
    * @param err_msg Текст ошибки
    * @param err_code Код ошибки
    """
    Miscellaneous.print_message(err_msg)
    Miscellaneous.print_message(f"Код ошибки: {err_code}")

def run_bot(api_token: str, http_proxy: str, https_proxy: str) -> None:
    """
    * Запуск Telegram-бота
    """
    Miscellaneous.print_message("Токен успешно определён.")
    bot: telebot = telebot.TeleBot(api_token)
    apihelper.proxy = {}  # создаём пустой словарь
    if not "".__eq__(http_proxy):
        apihelper.proxy['http'] = http_proxy
    if not "".__eq__(https_proxy):
        apihelper.proxy['https'] = https_proxy
    """
    * *************************
    * ОБРАБОТКА ЗАПРОСОВ ОТ ПОЛЬЗОВАТЕЛЯ
    * (НАЧАЛО)
    * *************************
    """
    @bot.message_handler(content_types=["text"])
    def text(message): # вся ботовская "кухня" запрятана здесь
        global cnt
        global MSG_NUMBER_LIMIT
        global GLOBAL_CODEPAGE
        global SETTINGS_FILE
        api_token: str = ""
        http_proxy: str = ""
        https_proxy: str = ""
        api_token, http_proxy, https_proxy = get_bot_config()
        Miscellaneous.print_message(f"Пользователь {message.from_user.id} (имя: {message.from_user.first_name}) оставил сообщение в Telegram: {chr(34)}{message.text}{chr(34)}.")
        if message.text == "hello":
            send_message(bot, message.chat.id, "И тебе hello!")
        if message.text == "/ip":
            local_ips = Miscellaneous.get_local_ip_addresses()
            if local_ips:
                send_message(bot, message.chat.id, "Локальные IP-адреса:")
                for ip in local_ips:
                    send_message(bot, message.chat.id, ip)
            else:
                send_message(bot, message.chat.id, "Не удалось получить локальные IP-адреса.")
        if message.text == "/username":
            send_message(bot, message.chat.id, Miscellaneous.get_username())
        if (
            (message.text == "/ps")
            or (message.text == "/process")
            or (message.text == "/processes")
        ):
            cnt = 0
            processes = Miscellaneous.get_running_processes()
            for process_name in processes:
                if cnt >= MSG_NUMBER_LIMIT:
                    break
                send_message(bot, message.chat.id, process_name)
                cnt += 1
            send_message(bot, message.chat.id, f"Общее количество процессов: {len(processes)}.")
        if (
            (message.text == "/date")
            or (message.text == "/time")
        ):
            send_message(bot, message.chat.id, f"Текущая дата: {Miscellaneous.get_current_time()}.")
        if (
            (message.text.lower() == "/help")
            or (message.text == "/?")
        ):
            send_message(bot, message.chat.id, "Команды, допустимые для использования: /ip, /username, /ps, /process, /processes, /date, /time, /help, /?, /quit, /stop, /exit, /ver, /sys, /printenv, /phrase, /send, /weather, /outer_ip")
        if (
            (message.text == "/ver")
            or (message.text == "/sys")
        ):
            sys_prop = Miscellaneous.get_system_properties()
            send_message(bot, message.chat.id, f"ОС: {sys_prop[0]}, версия {sys_prop[1]}, релиз {sys_prop[2]}. ОЗУ: всего: {sys_prop[3]}; используется: {sys_prop[4]}; свободно: {sys_prop[5]}; процент использования: {sys_prop[6]}.")
        if message.text == "/printenv":
            environment_variables = os.environ
            cnt = 0
            for key, value in environment_variables.items():
                if cnt >= MSG_NUMBER_LIMIT:
                    break
                send_message(bot, message.chat.id, f"{key}: {value}")
                cnt += 1
        if message.text == "/phrase":
            phrase: str = Miscellaneous.get_phrase_outta_file("phrase.txt", GLOBAL_CODEPAGE)
            if not "".__eq__(phrase):
                send_message(bot, message.chat.id, phrase)
            else:
                send_message(bot, message.chat.id, "Увы, фразы не заготовил.")
        if (
            (message.text == "/send")
            or (message.text.strip().startswith("/send "))
        ):
            v_send: str = message.text
            if v_send == "/send":
                send_message(bot, message.chat.id, f"Команду {chr(34)}send{chr(34)} нужно вызывать с передачей ей идентификатора получателя и текстом сообщения. Пример вызова: /send --user_id 03007 --msg Привет!_Как_у_тебя_дела?")
                send_message(bot, message.chat.id, "Строка должна быть неразрывной, вместо пробелов следует использовать символ подчёркивания.")
            else:
                v_send = v_send[len("/send "):].strip()
                print(v_send)
                send_parser = argparse.ArgumentParser(description="Отправка сообщения")
                send_parser.add_argument("--user_id", type=int, help="Идентификатор получателя", required=True, dest="user_id")
                send_parser.add_argument("--msg", type=str, help="Текст сообщения для получателя", required=True, dest="message")
                try:
                    send_args = send_parser.parse_args(v_send.split())
                    send_message(bot, message.chat.id, "Отправка сообщения пользователю...")
                    send_message(bot, send_args.user_id, send_args.message)
                    send_message(bot, message.chat.id, "Сообщение отправлено пользователю.")
                except SystemExit:
                    send_message(bot, message.chat.id, f"Ошибка в команде {chr(34)}send{chr(34)}.")
                    send_message(bot, message.chat.id, f"Введите {chr(34)}/send{chr(34)}, чтобы узнать, как правильно использовать команду.")
        if message.text == "/weather":
            weather_lines = Miscellaneous.get_url("https://wttr.in/?0T", http_proxy, https_proxy)
            if weather_lines:
                send_message(bot, message.chat.id, "Получен прогноз погоды. Данные представлены ниже.")
                for weather_line in weather_lines:
                    send_message(bot, message.chat.id, weather_line)
            else:
                send_message(bot, message.chat.id, "Прогноз погоды недоступен в данный момент времени.")
        if message.text == "/outer_ip":
            outer_ip_lines = Miscellaneous.get_url("https://icanhazip.com", http_proxy, https_proxy)
            if outer_ip_lines:
                send_message(bot, message.chat.id, "Получены данные по внешнему IP-адресу. Они представлены ниже.")
                for outer_ip_line in outer_ip_lines:
                    send_message(bot, message.chat.id, outer_ip_line)
            else:
                send_message(bot, message.chat.id, f"Невозможно определить {chr(34)}белый{chr(34)} IP-адрес.")
        if ( # команда завершения работы бота
            (message.text.lower() == "/quit")
            or (message.text.lower() == "/stop")
            or (message.text.lower() == "/exit")
        ):
            send_message(bot, message.chat.id, "Goodbye, cruel world! Никогда больше к вам не вернусь.")
            bot.stop_poll
            os._exit(0)
    """
    * *************************
    * ОБРАБОТКА ЗАПРОСОВ ОТ ПОЛЬЗОВАТЕЛЯ
    * (КОНЕЦ)
    * *************************
    """
    Miscellaneous.print_message("Telegram-бот запущен и ожидает команд пользователя в мессенджере.")
    Miscellaneous.print_message("Для остановки программы нажмите Ctrl+C в текущем сеансе или введите /quit в Telegram.")
    try:
        bot.polling(none_stop=False, interval=0)
    except KeyboardInterrupt: # перехват Ctrl+C
        pass
    except ProxyError as err_proxy:
        print_error("Произошла ошибка proxy-сервера.", f"{err_proxy}")
    except ApiTelegramException as err_api:
        print_error("Произошла ошибка доступа к Telegram API.", f"{err_api}")
    except ReadTimeout as err_read:
        print_error("Слишком большое время отклика от сервера Telegram.", f"{err_read}")
    return

def main() -> None:
    global SETTINGS_FILE
    api_token: str = ""
    http_proxy: str = ""
    https_proxy: str = ""
    Miscellaneous.print_message("Запуск Telegram-бота...")
    if Miscellaneous.is_file_readable(SETTINGS_FILE):
        Miscellaneous.print_message(f"Файл настроек найден: {SETTINGS_FILE}")
        api_token, http_proxy, https_proxy = get_bot_config()
    else:
        Miscellaneous.print_message(f"Ошибка: Файл настроек не найден: {SETTINGS_FILE}")
    if "".__eq__(api_token):
        Miscellaneous.print_message("Токен для Telegram-бота не найден.")
    else:
        run_bot(api_token, http_proxy, https_proxy)
    Miscellaneous.print_message("Завершение работы Telegram-бота.")
    return

# Точка запуска программы
if __name__ == "__main__":
    main()
