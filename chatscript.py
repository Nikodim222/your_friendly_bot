"""
* Класс для обеспечения функционирования клиента ChatScript
* *************************
* В данном классе содержится весь необходимый функционал для
* обеспечения работоспособности бота в сети IRC (RFC 1459).
* Для работы программы требуется Python 3.
* https://github.com/ChatScript/ChatScript
* Программа является кроссплатформенной. Она должна работать
* под Microsoft Windows, Linux, macOS и т.д.
*
* @author Ефремов А. В., 27.08.2025
"""

from socket import socket, AF_INET, SOCK_STREAM, timeout, gaierror
from collections import namedtuple
import re

ConnChatScript = namedtuple("ConnChatScript", ["host", "port", "timeout", "bot_name", "username"])
DEFAULT_HOST: str = "localhost"
DEFAULT_PORT: int = 1024
CODEPAGE: str = "utf-8"
NULL_BYTE = b'\x00'

class ChatScript:

    conn: ConnChatScript = None

    def __init__(self, server_host: str = DEFAULT_HOST, server_port: int = DEFAULT_PORT, timeout: float = 300, bot_name: str = "", username: str = "console_user"):
        self.conn = ConnChatScript(
            server_host if not "".__eq__(server_host) else DEFAULT_HOST,
            server_port if not (server_port < 1 or server_port > 65534) else DEFAULT_PORT,
            timeout,
            bot_name, username
        )

    def send_message(self, message_text: str) -> str:
        """
        * Отправка сообщения на сервер ChatScript и получение ответа от сервера
        *
        * @param message_text Текст отправляемого сообщения
        * @return Текст сообщения от сервера
        """
        if self.conn is not None:
            try:
                message_to_send = (self.conn.username.encode(CODEPAGE) + NULL_BYTE + self.conn.bot_name.encode(CODEPAGE) + NULL_BYTE + message_text.encode(CODEPAGE) + NULL_BYTE)
                with socket(AF_INET, SOCK_STREAM) as sock:
                    sock.settimeout(self.conn.timeout)
                    sock.connect((self.conn.host, self.conn.port))
                    sock.sendall(message_to_send)
                    response_bytes = b''
                    while True:
                        try:
                            chunk = sock.recv(128) # читаем по 128 байт
                            if not chunk: # соединение закрыто сервером
                                break
                            response_bytes += chunk
                        except timeout:
                            return "Timeout occurred while receiving data."
                        except ConnectionResetError:
                            return "Connection reset by peer."
                    return response_bytes.decode(CODEPAGE, errors='replace')
            except gaierror:
                return f"Error: Address-related error occurred. Could not resolve host '{self.conn.host}'."
            except ConnectionRefusedError:
                return f"Error: Connection refused. Is the ChatScript server running at {self.conn.host}:{self.conn.port}?"
            except timeout:
                return "Error: Connection timed out."
            except BrokenPipeError:
                return "Error: Broken pipe. The connection was unexpectedly closed."
            except Exception as e:
                return f"An error occurred: {e}"

    def is_command(self, input_string: str) -> bool:
        """
        * Проверяет, является ли входная строка командой ChatScript
        *
        * @param input_string Строка для проверки
        * @return True, если строка является командой, False в противном случае
        """
        command_pattern = re.compile(r'^:[a-zA-Z]+(\s+.*)?$')
        return bool(command_pattern.match(input_string))

    def send_user_message(self, message_text: str) -> str:
        """
        * Пользовательское сообщение для сервер ChatScript
        *
        * @param message_text Текст отправляемого сообщения
        * @return Текст сообщения от сервера
        """
        reply: str = ""
        if not self.is_command(message_text): # если не команда, то отправляем на сервер
            reply = self.send_message(message_text)
        return reply

    def is_server_running(self) -> bool:
        """
        * Проверка доступности сервера ChatScript
        *
        * @return True, если сервер работает, False в противном случае
        """
        is_running: bool = False
        if self.conn is not None:
            sock = socket(AF_INET, SOCK_STREAM)
            try:
                sock.settimeout(self.conn.timeout)
                sock.connect((self.conn.host, self.conn.port))
                is_running = True
            except Exception as e:
                pass
            finally:
                sock.close()
        return is_running

    def server_clearlog(self) -> str:
        """
        * System Control commands: Erase user log file
        *
        * @return Текст сообщения от сервера
        """
        return self.send_message(":clearlog")

    def server_quit(self) -> str:
        """
        * System Control commands: Exit ChatScript
        *
        * @return Текст сообщения от сервера
        """
        return self.send_message(":quit")

    def server_reset(self) -> str:
        """
        * System Control commands: Start user all over again, flushing his history
        *
        * @return Текст сообщения от сервера
        """
        return self.send_message(":reset")

    def server_restart(self) -> str:
        """
        * System Control commands: Restart ChatScript
        *
        * @return Текст сообщения от сервера
        """
        return self.send_message(":restart")
