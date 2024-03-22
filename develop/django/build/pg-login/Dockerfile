FROM postgres:12.17-alpine3.19

# Copiar el script de entrada y establecer permisos de ejecución
COPY ./tools/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN apk add --update && apk add curl
RUN apk update && apk add --upgrade jq

USER postgres
RUN chmod 700 -R /var/lib/postgresql/data

ENTRYPOINT ["/entrypoint.sh"]

