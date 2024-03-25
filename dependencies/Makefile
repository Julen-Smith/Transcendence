COMPOSE=docker compose -f docker-compose.yml

.PHONY: all clean down fclean ps re vault

all:
	$(COMPOSE) up -d $(SER)
	@sleep 1
	$(COMPOSE) exec vault /docker-entrypoint/init.sh sh

build:
	$(COMPOSE) build $(SER)

vault:
	$(COMPOSE) up -d vault
	@sleep 5
	$(COMPOSE) exec vault /docker-entrypoint/init.sh sh

clean: down rm
	VOLUMES=$$(docker volume ls -q | awk '/^core/')
	
	ifeq ($(VOLUMES))
	docker volume rm $$(docker volume ls -q | awk '/^core/')
	endif

down:
	$(COMPOSE) down $(SER)

rm:
	$(COMPOSE) rm $(SER)

ps:
	$(COMPOSE) ps $(SER)

stop:
	$(COMPOSE) stop $(SER)

live:
	$(COMPOSE) up

follow:
	$(COMPOSE) logs --follow --tail 200 $(SER)
