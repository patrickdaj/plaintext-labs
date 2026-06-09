# Module 04 — Windows Artifacts lab.
# Standard targets: up / down / reset / demo / shell
.PHONY: up down reset demo shell

up:  ## Build and start the chainsaw + python-registry container
	docker compose up -d --build

down:  ## Stop and remove the container
	docker compose down

reset:  ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:  ## Open a shell in the lab container
	docker compose exec lab bash

demo:  ## Parse bundled EVTX events and registry hive; print key forensic findings
	docker compose run --rm lab python3 parse_artifacts.py
