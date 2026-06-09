.PHONY: up down reset demo shell

OLLAMA_MODEL ?= tinyllama

up:        ## Build and start Ollama + lab containers
	docker compose up -d
	@echo "Pulling model $(OLLAMA_MODEL)..."
	@docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 -c " \
import requests, time; \
host=\"http://ollama:11434\"; \
for i in range(30): \
    try: requests.get(host+\"/api/tags\", timeout=2); break \
    except: time.sleep(2) \
print(\"Ollama ready. Pulling model...\"); \
r = requests.post(host+\"/api/pull\", json={\"name\":\"$(OLLAMA_MODEL)\"}, stream=True, timeout=600); \
[print(l.decode().strip()) for l in r.iter_lines() if l]; \
print(\"Done.\") \
"'

down:      ## Stop containers
	docker compose down

reset:     ## Tear down completely
	docker compose down --rmi local --volumes --remove-orphans

shell:     ## Open a shell in the lab container
	docker compose exec lab bash

demo:      ## Run all benchmark prompts and print results table
	docker compose run --rm lab sh -c '\
		pip install -q requests 2>/dev/null; \
		python3 -u - <<'"'"'PYEOF'"'"' \
import requests, time, sys; \
host = "http://ollama:11434"; \
model = "$(OLLAMA_MODEL)"; \
prompts_file = "data/benchmark-prompts.txt"; \
\
# Parse prompt blocks \
with open(prompts_file) as f: \
    raw = f.read(); \
blocks = [b.strip() for b in raw.split("---") if b.strip() and not b.strip().startswith("#")]; \
prompts = []; \
for b in blocks: \
    lines = b.splitlines(); \
    label = lines[0].strip(); \
    text = " ".join(l for l in lines[1:] if l.strip()); \
    prompts.append((label, text)); \
\
print(f"=== Benchmark: {model} ===\n"); \
print(f"{'#':<3} {'Prompt':<35} {'Latency':>10} {'Tokens':>8} {'tok/s':>8}"); \
print("-" * 70); \
for i, (label, prompt) in enumerate(prompts, 1): \
    t0 = time.time(); \
    r = requests.post(host+"/api/generate", json={"model":model,"prompt":prompt,"stream":False}, timeout=300); \
    elapsed = time.time() - t0; \
    data = r.json(); \
    toks = data.get("eval_count", 0); \
    throughput = toks / elapsed if elapsed > 0 else 0; \
    short = label.replace("PROMPT_","#"); \
    ans_preview = data.get("response","").strip().replace("\n"," ")[:80]; \
    print(f"{i:<3} {label:<35} {elapsed:>9.1f}s {toks:>8} {throughput:>7.1f}"); \
    print(f"    Answer: {ans_preview}..."); \
    print(); \
print("Copy the table above into results/benchmark-results.md"); \
PYEOF'
