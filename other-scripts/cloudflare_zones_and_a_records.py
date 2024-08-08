import requests

# Укажите ваш API токен Cloudflare и email
API_TOKEN = '5jYrDJbwtaYaSMTX1RCbd5u0Ew7x-FON4i9UIXRa'  # Замените на ваш API токен
API_EMAIL = 'd.kovalev@napoleonit.ru'  # Замените на ваш email

# Заголовки для авторизации
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# URL для получения всех зон
base_url = "https://api.cloudflare.com/client/v4"

# Функция для получения всех зон
def get_zones():
    url = f"{base_url}/zones"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверка на ошибки HTTP
    zones = response.json().get('result', [])
    return zones

# Функция для получения A-записей для определенной зоны
def get_a_records(zone_id):
    url = f"{base_url}/zones/{zone_id}/dns_records?type=A"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    a_records = response.json().get('result', [])
    return a_records

# Основная часть скрипта
def main():
    zones = get_zones()
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print(f"Зона: {zone_name}")

        a_records = get_a_records(zone_id)
        if a_records:
            print("A-записи:")
            for record in a_records:
                print(f"  - {record['name']} -> {record['content']}")
        else:
            print("  Нет A-записей")
        print()

if __name__ == "__main__":
    main()
