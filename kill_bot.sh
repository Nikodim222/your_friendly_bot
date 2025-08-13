#!/bin/sh
export http_proxy=
export https_proxy=

# полный путь до скрипта
export ABSOLUTE_FILENAME=`readlink -e "$0"`
# каталог, в котором лежит скрипт
export DIRECTORY=`dirname "$ABSOLUTE_FILENAME"`
cd $DIRECTORY

echo '************'
echo 'ПО "Твой дружелюбный бот"'
echo '************'

read -p "Вы собираетесь остановить работу бота. Продолжить? [Y/N] " confirm
if [[ "$confirm" == "Y" || "$confirm" == "y" ]]; then
  ps -f -u "$USER" | grep -e "run_bot.sh" -e "main.py" | grep -v "grep" | awk '{print $2}' | xargs kill
  echo "Бот выгружен из памяти."
else
  echo "Операция остановки бота отменена."
fi
