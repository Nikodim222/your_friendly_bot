ПО "Твой дружелюбный бот"
*************************

ОПИСАНИЕ

Программа является ботом для сервиса "Telegram". Написана она
на языке программирования Python 3 (http://python.org).
Программа кроссплатформенная.


ПРЕДВАРИТЕЛЬНЫЕ ТРЕБОВАНИЯ

Перед первым запуском рекомендуется выполнить следующие команды:

$ pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip
$ pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org configparser
$ pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org psutil

Программу можно получить из репозитория GitHub. В простейшем случае
это делается так:

$ git clone https://github.com/Nikodim222/your_friendly_bot.git

Если же у Вас выход в глобальную сеть идёт через proxy-сервер, то
программу можно получить так:

git clone https://github.com/Nikodim222/your_friendly_bot.git --config "http.proxy=http://proxy.local:8080"

Вместо подстроки "http://proxy.local:8080" в указанном выше примере
подставьте свой адрес proxy-сервера.


ФАЙЛ НАСТРОЕК ПРОГРАММЫ
             
Обратите внимание на то, что в директории с программой должен
находиться файл "settings.ini". Пример его содержимого:

[global]
; a token for accessing the HTTP API
api_token = your_Telegram_token_here

[proxy]
; либо пишется proxy, либо пишется слово DIRECT
; proxy-сервер нужно указать для протокола HTTP и HTTPS
http = http://proxy.local:8080
https = http://proxy2.local:8080

Если соединение используется прямое (без прокси) для выбранного протокола,
то тогда надо указать слово "DIRECT". Например:

[proxy]
; либо пишется proxy, либо пишется слово DIRECT
; proxy-сервер нужно указать для протокола HTTP и HTTPS
http = DIRECT
https = http://proxy2.local:8080

Файл "settings.ini" хранит данные в кодировке Windows-1251 (CP1251).


ЗАПУСК ПРОГРАММЫ

Для запуска из-под Microsoft Windows предусмотрен файл "run_bot.bat".
Для запуска программы под Linux предусмотрен файл "run_bot.sh".

-- EOF
