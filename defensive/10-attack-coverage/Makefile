# Module 10 — ATT&CK Mapping & Coverage lab.
.PHONY: up down reset shell demo
up:
	docker compose up -d --build
down:
	docker compose down
reset:
	docker compose down --rmi local --volumes --remove-orphans
shell:
	docker compose exec lab bash
demo:
	docker compose run --rm lab python coverage.py
