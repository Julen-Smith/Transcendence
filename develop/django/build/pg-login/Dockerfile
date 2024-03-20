FROM postgres:12.17-alpine3.19

# Copiar el script de entrada y establecer permisos de ejecución
COPY ./tools/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chmod 700 -R /var/lib/postgresql/data
RUN apk add --update && apk add curl
RUN apk update && apk add --upgrade jq


# Hacer la petición para obtener las variables de entorno y guardarlas en un archivo JSON
RUN curl -k --header "X-Vault-Token: hvs.in3sp3WYRgSpyNDDb5mFHGJc" --request GET https://195.35.48.173:8200/v1/transcendence/data/postgres_db > /tmp/secrets.json

# Extraer las variables de entorno del archivo JSON y exportarlas
RUN export $(jq -r '.data.data | to_entries | .[] | "\(.key)=\(.value)"' /tmp/secrets.json)

USER postgres

ENTRYPOINT ["/entrypoint.sh"]

#ENTRYPOINT ["tail", "-f"]