FROM python:alpine3.18 

ARG VAULT_TOKEN

RUN apk add --update bash sudo build-base libpq-dev curl

COPY tools/docker-entrypoint.sh docker-entrypoint.sh

COPY tools/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copiar el script de entrada y establecer permisos de ejecución
COPY ./tools/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ARG ADMIN=transcendence

# VARIABLES DE ENTORNO DESDE VAULT -Hacer la petición para obtener las variables de entorno y guardarlas en un archivo JSON
RUN mkdir secrets 
#Secrets 'login'
RUN sudo curl  -k --header "X-Vault-Token: ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/login_google > secrets/login_google_secrets.json
RUN sudo curl  -k --header "X-Vault-Token: ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/login_intra > secrets/login_intra_secrets.json
#Secrets 'tools'
#RUN sudo curl -k --header "X-Vault-Token:  ${VAULT_TOKEN}"  --request GET  https://127.0.0.1:8200/v1/transcendence/data/tools > secrets/tools_secrets.json
# #Secrets 'jwt' 
RUN sudo curl  -k --header "X-Vault-Token: ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/JWT > secrets/jwt_secrets.json
# #Secrets 'postgres' 
RUN sudo curl  -k --header "X-Vault-Token: ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/postgres_db > secrets/postgres_db_secrets.json

#logger
RUN sudo curl -k --header "X-Vault-Token: ${VAULT_TOKEN}"  --request GET  https://65.109.174.85:8200/v1/transcendence/data/logger > secrets/logger_secrets.json

# add new user
RUN adduser -D -s /bin/bash $ADMIN \
        && mkdir -p /etc/sudoers.d \
        && echo "$ADMIN ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$ADMIN \
        && chmod 0440 /etc/sudoers.d/$ADMIN

USER $ADMIN

ENTRYPOINT [ "./docker-entrypoint.sh" ]
