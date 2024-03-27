#!/bin/bash

# Задайте путь к вашему репозиторию
REPO_PATH="/home/dkovalev/Документы/sh"

# Переходим в директорию репозитория
cd $REPO_PATH

# Проверяем статус репозитория
git status

# Если есть изменения, то добавляем их и делаем коммит
if [[ $(git status -s) ]]
then
    git add .
    # Получаем текущую дату и время
    NOW=$(date +"%m-%d-%Y %T")
    # Добавляем дату и время в сообщение коммита
    git commit -m "Auto-commit on $NOW"
    git push origin master
else
    echo "No changes to commit"
fi