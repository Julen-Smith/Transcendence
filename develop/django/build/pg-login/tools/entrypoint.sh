#!/bin/bash

# Esperar 10 segundos para asegurarse de que el servidor de PostgreSQL esté listo
sleep 10

# Verificar y ajustar los permisos del directorio de datos
chown -R postgres:postgres /var/lib/postgresql/data
chmod 700 /var/lib/postgresql/data

# Hacer la petición para obtener las variables de entorno y guardarlas en un archivo JSON
curl -k --header "X-Vault-Token: ${VAULT_TOKEN}" --request GET https://195.35.48.173:8200/v1/transcendence/data/postgres_db > /tmp/secrets.json

# Extraer las variables de entorno del archivo JSON y exportarlas
eval $(jq -r '.data.data | to_entries | .[] | "export \(.key)=\(.value | @json)"' /tmp/secrets.json)

# Crear la base de datos si no existe
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || psql -U postgres -c "CREATE DATABASE \"$POSTGRES_DB\";"

# Crear el usuario si no existe
psql -U postgres -tc "SELECT 1 FROM pg_roles WHERE rolname = '$POSTGRES_USER'" | grep -q 1 || psql -U postgres -c "CREATE USER \"$POSTGRES_USER\" WITH PASSWORD '$POSTGRES_PASSWORD';"

# Asignar todos los privilegios al usuario sobre la base de datos
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE \"$POSTGRES_DB\" TO \"$POSTGRES_USER\";"

# Ejecutar el servidor de PostgreSQL
exec postgres