#!/bin/bash

# Получите Server ID из файла
server_id=$(cat /opt/atlassian/jira/server_id.txt)

# Получите ключ активации из atlassian-agent.jar
activation_key=$(java -jar /opt/atlassian/atlassian-agent.jar -mail "$JIRA_ADMIN_EMAIL" -n "My Jira" -o "My Company" -p jira -s "$server_id")

# Активируйте Jira
curl -X POST -H "Content-Type: application/json" \
     -d "{\"licenseKey\":\"$activation_key\",\"siteTitle\":\"My Jira Site\",\"baseUrl\":\"http://localhost:8080\",\"adminEmail\":\"$JIRA_ADMIN_EMAIL\",\"adminPassword\":\"$JIRA_ADMIN_PASSWORD\"}" \
     http://localhost:8080/rest/api/1.0/application-properties/license

echo "Jira has been activated!"

# Запустите Jira
/opt/atlassian/jira/bin/start-jira.sh
