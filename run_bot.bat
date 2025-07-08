@Echo Off
chcp 65001>nul

Echo ************
Echo ПО "Твой дружелюбный бот"
Echo ************

Set http_proxy=
Set https_proxy=

setlocal enabledelayedexpansion
Set count=0
for /f "tokens=*" %%i in ('where python.exe ^| findstr "Python3"') do (
  Set /a count+=1
  Set pythop_file=%%i
  if !count! GEQ 3 goto :break_loop
)
:break_loop
endlocal /b && Set pythop_file=%pythop_file%

if not defined pythop_file goto :no_python
if "%pythop_file%"=="" goto :no_python
if not exist "%pythop_file%" goto :no_python

for %%a in ("%pythop_file%") do (
  Set "py=%%~dpa"
)

if "%py:~-1%"=="\" (
  if not "%py%"=="%py:~0,2%\" (
    Set "py=%py:~0,-1%"
  )
)

rem Echo Python 3 располагается в директории:
rem Echo %py%

rem Путь до Python 3
Set PATH=%py%;%PATH%

cd /D "%~dp0"

:loop
python .\main.py
goto :loop
:q
exit

:no_python
echo Python 3 не найден.
goto :q
