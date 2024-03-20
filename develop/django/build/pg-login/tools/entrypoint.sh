#!/bin/bash

# Hacer la petición para obtener las variables de entorno y guardarlas en un archivo JSON
curl -k --header "X-Vault-Token: hvs.Dd77um8uAHucsxDQwx6RQSoz" --request GET https://195.35.48.173:8200/v1/transcendence/data/postgres_db > /tmp/secrets.json

# Verificar el contenido del archivo secrets.json
echo "Contenido del archivo secrets.json:"
cat /tmp/secrets.json

# Extraer las variables de entorno del archivo JSON y exportarlas
eval $(jq -r '.data.data | to_entries | .[] | "export \(.key)=\(.value | @json)"' /tmp/secrets.json)

# Verificar si las variables de entorno se han exportado correctamente
echo "Variables de entorno exportadas:"
env



# Ejecutar el comando por defecto// NO FUNCIONA
exec postgres