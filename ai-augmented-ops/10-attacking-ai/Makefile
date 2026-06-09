.PHONY: up down reset demo shell garak-fast garak-full promptfoo-eval

OLLAMA_MODEL ?= tinyllama

up:        ## Start Ollama + garak + promptfoo containers and pull model
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

shell:     ## Open a shell in the garak container
	docker compose exec garak bash

demo:      ## Run fast garak scan (injection + leakage probes only)
	@echo "=== garak Fast Scan — injection + leakage probes ==="
	@echo "This scans for prompt injection resistance and system prompt leakage."
	@echo "Full scan (all probes): make garak-full"
	@echo ""
	$(MAKE) garak-fast

garak-fast:   ## Run garak with injection + leakage probes only (~5-10 min)
	docker compose run --rm garak \
		python -m garak \
		--model_type ollama \
		--model_name $(OLLAMA_MODEL) \
		--probes injection,leakage \
		--report_prefix /lab/results/garak-fast 2>&1 | tee results/garak-raw.txt
	@echo ""
	@echo "Results written to results/garak-raw.txt"
	@echo "Review: copy the probe summary table into results/garak-findings.md"

garak-full:   ## Run garak with all probe classes (~30-60 min)
	@echo "WARNING: Full scan takes 30-60 minutes on CPU. Running in background."
	docker compose run --rm garak \
		python -m garak \
		--model_type ollama \
		--model_name $(OLLAMA_MODEL) \
		--report_prefix /lab/results/garak-full 2>&1 | tee results/garak-full-raw.txt

promptfoo-eval:  ## Run promptfoo evaluation against attack-prompts.yaml
	@echo "=== promptfoo Adversarial Evaluation ==="
	docker compose run --rm promptfoo \
		promptfoo eval \
		--config /lab/data/attack-prompts.yaml \
		--output /lab/results/promptfoo-results.json 2>&1 | tee results/promptfoo-raw.txt
	@echo ""
	@echo "Results written to results/promptfoo-results.json"
	@echo "Review failing assertions and add analysis to results/promptfoo-findings.md"
