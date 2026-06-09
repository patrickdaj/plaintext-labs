.PHONY: up down reset demo shell

OLLAMA_MODEL ?= tinyllama

up:        ## Build and start Ollama + lab containers
	docker compose up -d
	@echo "Pulling model $(OLLAMA_MODEL) — this may take a few minutes on first run..."
	@docker compose exec ollama ollama pull $(OLLAMA_MODEL) 2>/dev/null || \
		docker compose run --rm lab sh -c \
		  'until curl -sf http://ollama:11434/api/tags >/dev/null; do sleep 2; done; \
		   curl -s http://ollama:11434/api/pull -d "{\"name\":\"$(OLLAMA_MODEL)\"}" | tail -1'

down:      ## Stop containers
	docker compose down

reset:     ## Tear down completely (containers + model cache volume)
	docker compose down --rmi local --volumes --remove-orphans

shell:     ## Open a shell in the lab container
	docker compose exec lab bash

demo:      ## Ask tinyllama one security question and show latency + token rate
	@echo "=== Hybrid AI Pattern — Demo ==="
	@echo "Model: $(OLLAMA_MODEL)  |  Host: http://ollama:11434"
	@echo ""
	docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 -c " \
import requests, time, json; \
prompt = \"You are a security analyst. A Windows host generated this event: process cmd.exe spawned by winword.exe with argument /c powershell -enc ZQBjAGgAbwAgAHQAZQBzAHQ=. In one sentence, what ATT&CK technique does this suggest and what is your recommended immediate action?\"; \
start = time.time(); \
r = requests.post(\"http://ollama:11434/api/generate\", json={\"model\":\"$(OLLAMA_MODEL)\",\"prompt\":prompt,\"stream\":False}, timeout=120); \
elapsed = time.time() - start; \
data = r.json(); \
print(\"PROMPT:\", prompt[:120], \"...\"); \
print(); \
print(\"ANSWER:\", data.get(\"response\",\"\").strip()); \
print(); \
toks = data.get(\"eval_count\", 0); \
print(f\"Latency: {elapsed:.1f}s | Tokens generated: {toks} | Throughput: {toks/elapsed:.1f} tok/s\"); \
print(); \
print(\"NOTE: Review the answer critically. Would you act on it without verification?\"); \
"'
