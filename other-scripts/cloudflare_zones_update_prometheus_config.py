import requests
import yaml
import time
import os

# Настройки
API_TOKEN = '5jYrDJbwtaYaSMTX1RCbd5u0Ew7x-FON4i9UIXRa'  # Замените на ваш API токен
API_EMAIL = 'd.kovalev@napoleonit.ru'  # Замените на ваш email
PROMETHEUS_FILE = 'other_domains.yml'  # Путь к файлу конфигурации Prometheus
RATE_LIMIT = 200  # Лимит запросов в минуту
DELAY = 60 / RATE_LIMIT  # Задержка между запросами (в секундах)
LOG_FILE = '/var/log/prometheus/prometheus_targets_update.log'  # Путь к файлу логов
TEMP_FILE = '/tmp/prometheus_targets_temp.yml'  # Определение переменных

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

# Функция для очистки и форматирования доменов
def clean_domain(domain_name):
    # Убираем префикс 'www.'
    if domain_name.startswith("www."):
        domain_name = domain_name[4:]

    # Удаляем начальные точки и звездочки
    domain_name = domain_name.lstrip('.').lstrip('*').lstrip('.')
    
    # Удаляем '.*'
    if domain_name.startswith("*"):
        domain_name = domain_name[1:]
    
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

    # Запись в временный файл
    with open(TEMP_FILE, 'w') as f:
        yaml.dump(prometheus_config, f, default_flow_style=False)
    
    # Проверка временного файла
    try:
        with open(TEMP_FILE, 'r') as f:
            yaml.safe_load(f)
    except yaml.YAMLError as e:
        log(f"Ошибка YAML при проверке временного файла: {e}")
        return
    
    # Замена основного файла конфигурации
    os.rename(TEMP_FILE, PROMETHEUS_FILE)
    log(f"Конфигурация Prometheus обновлена в {PROMETHEUS_FILE}")

# Функция для записи логов
def log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# Основной скрипт
def main():
    log("Обновление данных и конфигурации Prometheus начато")
    generate_prometheus_config()
    log("Обновление завершено")

if __name__ == "__main__":
    main()