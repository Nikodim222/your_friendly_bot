@Echo Off
chcp 65001>nul

Echo ************
Echo ПО "Твой дружелюбный бот"
Echo ************

Set http_proxy=
Set https_proxy=

rem Путь до Python 3
Set PATH=%LOCALAPPDATA%\Programs\Python\Python313;%PATH%

cd /D "%~dp0"

:loop
python .\main.py
goto loop
