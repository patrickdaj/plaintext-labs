.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec lab bash

demo:      ## Run full MISP workflow: create event, add IOCs, enrich, tag, publish
	docker compose run --rm lab python workflow.py
