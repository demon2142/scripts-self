#!/bin/bash

# Ожидание запуска базы данных
until PGPASSWORD=$JDBC_PASSWORD psql -h $JDBC_HOST -U $JDBC_USER -d $JDBC_DATABASE -c "SELECT 1;" &> /dev/null; do
  echo "Ожидание запуска базы данных..."
  sleep 5
done

# Создание схемы базы данных
PGPASSWORD=$JDBC_PASSWORD psql -h $JDBC_HOST -U $JDBC_USER -d $JDBC_DATABASE -c "
  CREATE SCHEMA IF NOT EXISTS jira;
  SET search_path TO jira;
"
