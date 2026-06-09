.PHONY: up down reset demo shell

OLLAMA_MODEL ?= tinyllama

up:        ## Start Ollama and pull the model
	docker compose up -d
	@docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 -c " \
import requests, time; \
host=\"http://ollama:11434\"; \
for i in range(30): \
    try: requests.get(host+\"/api/tags\", timeout=2); break \
    except: time.sleep(2) \
r = requests.post(host+\"/api/pull\", json={\"name\":\"$(OLLAMA_MODEL)\"}, stream=True, timeout=600); \
[print(l.decode().strip()) for l in r.iter_lines() if l] \
"'

down:      ## Stop containers
	docker compose down

reset:     ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:     ## Open a shell in the lab container
	docker compose exec lab bash

demo:      ## Run Pattern 5 (few-shot phishing classification) as a worked example
	@echo "=== Prompt Patterns Demo — Pattern 5: Few-Shot Classification ==="
	@echo "This demo shows the few-shot phishing classification pattern."
	@echo "Watch: does the model output match the expected 'LABEL: X — reason' format?"
	@echo ""
	docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 scripts/run-pattern.py --pattern 5 --model $(OLLAMA_MODEL)'
