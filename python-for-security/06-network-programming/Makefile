.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

shell:
	docker compose exec lab bash

demo:      ## Run reference scanner + banner grabber against the target container
	docker compose run --rm lab python scanner.py --host target --ports 22,80,443,8080,9999
