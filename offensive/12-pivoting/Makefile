.PHONY: up down reset shell demo

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec attacker bash

demo:
	docker compose run --rm attacker python3 pivot_demo.py
