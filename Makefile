THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help prod logs down ps up postgres
help:
	@echo "help\nprod\nup\nlogs\ndown\nps\npostgres"
prod:
	docker-compose -f gru5.yml build --no-cache
	docker-compose -f gru5.yml up -d
logs:
	docker-compose -f gru5.yml logs
down:
	docker-compose -f gru5.yml down
ps:
	docker-compose -f gru5.yml ps
up:
	docker-compose -f gru5.yml up -d
postgres:
	docker-compose -f gru5.yml exec db psql -Upostgres
