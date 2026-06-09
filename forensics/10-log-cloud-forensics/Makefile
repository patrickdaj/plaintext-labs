.PHONY: up down reset demo shell

up:
	docker compose up -d --build
	@echo "Container ready. Run 'make demo' to analyse EVTX and CloudTrail data."

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	docker compose exec lab sh /scripts/demo.sh

shell:
	docker compose exec lab bash
