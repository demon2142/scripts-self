FROM atlassian/jira-software:9.12.1

# Установите необходимые зависимости
RUN apt-get update && apt-get install -y \
    curl \
    jq \
    openjdk-11-jdk \
    openjdk-11-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

# Скопируйте скрипты и atlassian-agent.jar
COPY get_server_id.sh /var/atlassian/jira/bin/get_server_id.sh
#COPY activate_jira.sh /opt/atlassian/jira/bin/activate_jira.sh
COPY atlassian-agent.jar /var/atlassian/atlassian-agent.jar
RUN chmod +x /var/atlassian/atlassian-agent.jar
RUN chmod +x /var/atlassian/jira/bin/get_server_id.sh 
#/opt/atlassian/jira/bin/activate_jira.sh

# Сохраните Server ID в файл
#RUN /var/atlassian/jira/bin/get_server_id.sh > /var/atlassian/jira/server_id.txt

# Установите переменные окружения для активации
ENV JIRA_ADMIN_EMAIL=demon2142
ENV JIRA_ADMIN_PASSWORD=Tpyjhwxs

# Запустите скрипт активации при запуске контейнера
#CMD ["/opt/atlassian/jira/bin/activate_jira.sh"]
