#!/bin/bash

# Дождитесь запуска Jira
until $(curl --output /dev/null --silent --head --fail http://localhost:8080); do
    echo "Waiting for Jira to start..."
    sleep 5
done

# Получите Server ID
server_id=$(curl -s http://localhost:8080/rest/api/1.0/application-properties | jq -r '.serverId')
echo $server_id
