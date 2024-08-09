import requests
import yaml
import time

# Настройки
API_TOKEN = '5jYrDJbwtaYaSMTX1RCbd5u0Ew7x-FON4i9UIXRa'  # Замените на ваш API токен
API_EMAIL = 'd.kovalev@napoleonit.ru'  # Замените на ваш email
PROMETHEUS_FILE = 'targets.yml'  # Путь к файлу конфигурации Prometheus
RATE_LIMIT = 200  # Лимит запросов в минуту
DELAY = 60 / RATE_LIMIT  # Задержка между запросами (в секундах)

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

# Функция для очистки и формата доменов
def clean_domain(domain_name):
    # Убираем префикс 'www.' и все точки в начале
    if domain_name.startswith("www."):
        domain_name = domain_name[4:]
    
    # Удаляем начальные точки
    domain_name = domain_name.lstrip('.')

    return domain_name

# Функция для обновления Prometheus конфигурации
def generate_prometheus_config():
    zones = get_zones()
    https_targets = set()  # Используем set для уникальных записей

    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print(f"Зона: {zone_name}")
        
        a_records = get_a_records(zone_id)
        time.sleep(DELAY)  # Задержка между запросами для предотвращения превышения лимита

        for record in a_records:
            domain_name = record['name']
            # Очистка домена
            cleaned_domain = clean_domain(domain_name)
            if cleaned_domain:
                https_targets.add(f"https://{cleaned_domain}")

    prometheus_config = [{
        "labels": {
            "job": "blackbox_ssl_monitoring"
        },
        "targets": list(https_targets)
    }]

    with open(PROMETHEUS_FILE, 'w') as f:
        yaml.dump(prometheus_config, f, default_flow_style=False)
    
    print(f"Конфигурация Prometheus обновлена в {PROMETHEUS_FILE}")

# Основной скрипт
def main():
    print("Обновление данных и конфигурации Prometheus")
    generate_prometheus_config()
    print("Завершено.")

if __name__ == "__main__":
    main()