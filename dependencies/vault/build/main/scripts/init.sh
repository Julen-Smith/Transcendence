#!/bin/ash

nc -vz localhost 8200
retval=$?
while [ $retval -ne 0 ]; do

    sleep 1
    nc -vz localhost 8200
    retval=$?
    
done

i=0
vault operator init | while IFS= read -r line
do

    echo "$line" | grep "Unseal Key"
    if [ $? -eq 0 ]; then

        unseal_key=$(echo $line | awk '{ print $4 }')
        vault operator unseal $unseal_key
        i=$(($i+1))
        echo $unseal_key > ./unseal_key_$i

    else

        echo "$line" | grep "Root Token"
        if [ $? -eq 0 ]; then

            root_token=$(echo $line | awk '{ print $4 }')
            export VAULT_TOKEN=$root_token
            vault login $root_token
            vault secrets enable kv
            echo $root_token > ./root_token.txt
            break

        fi

    fi

done

vault kv put -mount=kv/login google google_client_id=$LOGIN_GOOGLE_CLIENT_ID \
google_client_secret=$LOGIN_GOOGLE_CLIENT_SECRET \
google_client_app_id=$LOGIN_GOOGLE_APP_ID

vault kv put -mount=kv/login jwt secret=$LOGIN_JWT_SECRET