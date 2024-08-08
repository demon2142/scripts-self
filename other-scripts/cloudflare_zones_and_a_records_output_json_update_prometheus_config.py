import requests
import json
import os
from datetime import datetime
from time import sleep

# Настройки
API_TOKEN = 'ваш_api_токен'  # Замените на ваш API токен
API_EMAIL = 'ваш_email'  # Замените на ваш email
CACHE_FILE = 'cloudflare_cache.json'
PROMETHEUS_FILE = '/etc/prometheus/targets.json'  # Путь к файлу конфигурации Prometheus
CHECK_INTERVAL = 86400  # Интервал проверки в секундах (86400 секунд = 1 день)

# Заголовки для авторизации
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

base_url = "https://api.cloudflare.com/client/v4"

# Функция для получения всех зон
def get_zones():
    url = f"{base_url}/zones"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('result', [])

# Функция для получения A-записей для определенной зоны
def get_a_records(zone_id):
    url = f"{base_url}/zones/{zone_id}/dns_records?type=A"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('result', [])

# Функция для обновления кэша и записи его в JSON файл
def update_cache():
    zones = get_zones()
    cache_data = {}

    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print(f"Зона: {zone_name}")

        a_records = get_a_records(zone_id)
        cache_data[zone_name] = a_records

    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_data, f, indent=4)

    print(f"Кэш обновлен и сохранен в {CACHE_FILE}")
    return cache_data

# Функция для генерации файла конфигурации Prometheus
def generate_prometheus_config(cache_data):
    targets = []

    for zone_name, a_records in cache_data.items():
        for record in a_records:
            targets.append({
                "targets": [record['name']],
                "labels": {"zone": zone_name}
            })

    with open(PROMETHEUS_FILE, 'w') as f:
        json.dump(targets, f, indent=4)

    print(f"Конфигурация Prometheus обновлена в {PROMETHEUS_FILE}")

# Основной цикл
def main():
    while True:
        print(f"Обновление данных: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        cache_data = update_cache()
        generate_prometheus_config(cache_data)
        print(f"Следующее обновление через {CHECK_INTERVAL / 3600} часов.")
        sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
