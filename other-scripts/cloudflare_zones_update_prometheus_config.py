import requests
import json

# Настройки
API_TOKEN = '5jYrDJbwtaYaSMTX1RCbd5u0Ew7x-FON4i9UIXRa'  # Замените на ваш API токен
API_EMAIL = 'd.kovalev@napoleonit.ru'  # Замените на ваш email
PROMETHEUS_FILE = 'targets.json'  # Путь к файлу конфигурации Prometheus

# Проверка на корректность токена и email
try:
    API_TOKEN.encode('latin-1')
    API_EMAIL.encode('latin-1')
except UnicodeEncodeError as e:
    print(f"Ошибка кодирования токена или email: {e}")
    exit(1)

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

# Функция для обновления Prometheus конфигурации
def generate_prometheus_config():
    zones = get_zones()
    targets = []
    
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print(f"Зона: {zone_name}")
        
        a_records = get_a_records(zone_id)
        
        for record in a_records:
            targets.append({
                "targets": [record['name']],
                "labels": {"zone": zone_name}
            })

    with open(PROMETHEUS_FILE, 'w') as f:
        json.dump(targets, f, indent=4)
    
    print(f"Конфигурация Prometheus обновлена в {PROMETHEUS_FILE}")

# Основной скрипт
def main():
    print("Обновление данных и конфигурации Prometheus")
    generate_prometheus_config()
    print("Завершено.")

if __name__ == "__main__":
    main()