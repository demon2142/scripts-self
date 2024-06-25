#!/bin/bash

# Получаем текущую версию пакета, установленного в системе
current_version=$(rpm -qa | grep tabby | awk -F'-' '{print "v"$3}')

# Получаем последнюю версию с GitHub
latest_version=$(curl -s https://api.github.com/repos/Eugeny/tabby/releases/latest | grep -o '"tag_name": *"[^"]*"' | head -n 1 | sed 's/"tag_name": *"//;s/"//')
latest_version_url=$(curl -s https://api.github.com/repos/Eugeny/tabby/releases/latest | grep -o '"tag_name": *"[^"]*"' | head -n 1 | sed 's/"tag_name": *"//;s/"//' | sed 's|v||')

# Сравниваем версии
if [[ "$current_version" < "$latest_version" ]]; then
    echo "Доступна новая версия tabby: $latest_version"


    # Скачиваем новый пакет
    package_name="tabby-$latest_version_url-linux-x64.rpm"
    download_url="https://github.com/Eugeny/tabby/releases/download/$latest_version/$package_name"
    wget $download_url

    # Устанавливаем новый пакет
    sudo epm -i $package_name
    rm $package_name
else
    echo "Установлена последняя версия tabby: $current_version"
fi
