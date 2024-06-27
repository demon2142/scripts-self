#!/bin/bash

# Дождитесь запуска Jira
until $(curl --output /dev/null --silent --head --fail http://localhost:8080); do
    echo "Waiting for Jira to start..."
    sleep 5
done

# Восстановите Jira из резервной копии
curl -X POST -H "Content-Type: multipart/form-data" \
     -F "attachment=@$JIRA_BACKUP_FILE" \
     -F "restoreOption=MERGE" \
     -F "overwritePermissions=true" \
     -F "overwriteIssueSecurityLevels=true" \
     http://localhost:8080/rest/backup/1/restore/import.json

echo "Jira has been restored from backup!"

# Запустите Jira
/opt/atlassian/jira/bin/start-jira.sh
