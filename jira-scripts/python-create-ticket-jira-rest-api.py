import requests
from requests.auth import HTTPBasicAuth
import json

# Параметры для подключения
jira_url = 'https://your-domain.atlassian.net'
jira_email = 'your-email@example.com'
jira_api_token = 'your-api-token'
project_key = 'PROJECT_KEY'

# Данные для задачи
issue_data = {
    'fields': {
        'project': {
            'key': project_key
        },
        'summary': '[Napoleon/Goal Profit] Python Developer (Junior/Middle)',
        'description': 'Описание задачи',
        'issuetype': {
            'name': 'Task'
        },
        'assignee': {
            'name': 'Albina'
        }
    }
}

# Создание задачи
response = requests.post(
    f'{jira_url}/rest/api/3/issue',
    headers={
        'Content-Type': 'application/json'
    },
    auth=HTTPBasicAuth(jira_email, jira_api_token),
    data=json.dumps(issue_data)
)

# Проверка результата
if response.status_code == 201:
    print('Задача успешно создана')
else:
    print(f'Ошибка создания задачи: {response.status_code}')
    print(response.json())
