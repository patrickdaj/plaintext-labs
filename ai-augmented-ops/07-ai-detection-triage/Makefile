.PHONY: up down reset demo shell triage eval

OLLAMA_MODEL ?= tinyllama

up:        ## Start Ollama and pull the model
	docker compose up -d
	@docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 -c " \
import requests, time; \
for i in range(30): \
    try: requests.get(\"http://ollama:11434/api/tags\", timeout=2); break \
    except: time.sleep(2) \
requests.post(\"http://ollama:11434/api/pull\", json={\"name\":\"$(OLLAMA_MODEL)\"}, timeout=600); \
print(\"Model ready.\") \
"'

down:      ## Stop containers
	docker compose down

reset:     ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:     ## Open a shell in the lab container
	docker compose exec lab bash

demo:      ## Triage 5 sample alerts and show model output vs ground truth
	@echo "=== Alert Triage Demo — 5 sample alerts ==="
	docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 scripts/triage.py --sample 5; \
		echo ""; \
		echo "Ground truth comparison:"; \
		python3 scripts/compare.py'

triage:    ## Triage all 50 alerts
	docker compose run --rm lab sh -c 'pip install -q requests 2>/dev/null && python3 scripts/triage.py'

eval:      ## Compute accuracy metrics against ground truth
	docker compose run --rm lab sh -c 'python3 scripts/eval.py'
