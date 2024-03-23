#!/bin/bash

# Verificar y ajustar los permisos del directorio de datos
chown -R postgres:postgres /var/lib/postgresql/data
chmod 750 /var/lib/postgresql/data

# Hacer la petición para obtener las variables de entorno y guardarlas en un archivo JSON
curl -k --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET https://195.35.48.173:8200/v1/transcendence/data/postgres_db > /tmp/secrets.json
chmod 777 /tmp/secrets.json

# Extraer las variables de entorno del archivo JSON y exportarlas
eval $(jq -r '.data.data | to_entries | .[] | "export \(.key)=\(.value | @json)"' /tmp/secrets.json)

# Ejecutar el servidor de PostgreSQL
exec /usr/local/bin/docker-entrypoint.sh postgres

