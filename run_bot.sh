#!/bin/sh
export http_proxy=
export https_proxy=

# полный путь до скрипта
export ABSOLUTE_FILENAME=`readlink -e "$0"`
# каталог, в котором лежит скрипт
export DIRECTORY=`dirname "$ABSOLUTE_FILENAME"`
cd $DIRECTORY


while true
do
  python3 ./main.py
done
