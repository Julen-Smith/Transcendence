FROM postgres:12.17-alpine3.19

RUN apk add --update && apk add curl
RUN apk update && apk add --upgrade jq
COPY ./tools/entrypoint.sh new_entrypoint.sh
RUN chmod 777 new_entrypoint.sh

ENTRYPOINT ["./new_entrypoint.sh"]

