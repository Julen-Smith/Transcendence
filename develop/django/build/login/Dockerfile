FROM python:alpine3.18

RUN apk add --update bash sudo build-base libpq-dev libffi-dev && mkdir -p /tools

RUN apk add --update && apk add curl

COPY ./tools/params.json /tools/params.json
COPY ./tools/logger.json /tools/logger.json
COPY ./tools/docker-entrypoint.sh docker-entrypoint.sh

COPY ./tools/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ARG ADMIN=transcendence
ARG PORT=25671
ARG VAULT_TOKEN
ARG WHAT=123

# VARIABLES DE ENTORNO DESDE VAULT -Hacer la petición para obtener las variables de entorno y guardarlas en un archivo JSON
RUN mkdir secrets 
#Secrets 'login'
RUN sudo curl  -k --header "X-Vault-Token:  ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/login_intra > secrets/login_intra_secrets.json
#Secrets 'login_google'
RUN sudo curl  -k --header "X-Vault-Token:  ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/login_google > secrets/login_google_secrets.json
#Secrets 'transcendence_server'
RUN sudo curl  -k --header "X-Vault-Token: ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/server > secrets/server.json
#Secrets 'tools'
#RUN sudo curl -k --header "X-Vault-Token:  ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/tools > secrets/tools_secrets.json

#logger
RUN sudo curl -k --header "X-Vault-Token:  ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/logger > secrets/logger_secrets.json
# #Secrets 'postgres' 
RUN sudo curl  -k --header "X-Vault-Token: ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/postgres_db > secrets/postgres_db_secrets.json

# add new user
RUN adduser -D -s /bin/bash $ADMIN \
        && mkdir -p /etc/sudoers.d \
        && echo "$ADMIN ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$ADMIN \
        && chmod 0440 /etc/sudoers.d/$ADMIN
USER $ADMIN

EXPOSE $PORT

ENTRYPOINT [ "./docker-entrypoint.sh" ]
