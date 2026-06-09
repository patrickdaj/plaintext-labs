# Local Model Benchmark Results
## Meridian Financial — AI Infrastructure Evaluation

**Date:** <!-- fill in -->
**Tester:** <!-- fill in -->
**Environment:** Docker on <!-- CPU/GPU, RAM -->

---

## Model card

| Field | Value |
|-------|-------|
| Model name | <!-- e.g. tinyllama --> |
| Parameter count | <!-- e.g. 1.1B --> |
| Quantisation | <!-- e.g. Q4_0 --> |
| Context length | <!-- e.g. 2048 tokens --> |
| Ollama image tag | <!-- e.g. ollama/ollama:0.3.14 --> |

---

## Benchmark results

| # | Prompt summary | Latency (s) | Tokens generated | Throughput (tok/s) | Quality | Notes |
|---|----------------|------------|------------------|--------------------|---------|-------|
| 1 | ATT&CK classification (encoded PS) | | | | Correct / Partial / Wrong | |
| 2 | CVE-2021-44228 summary | | | | Correct / Partial / Wrong | |
| 3 | Hypotheses for suspicious outbound | | | | Correct / Partial / Wrong | |
| 4 | Empty-file SHA-256 recognition | | | | Correct / Partial / Wrong | |
| 5 | Sigma rule generation | | | | Correct / Partial / Wrong | |

---

## Comparison (optional — larger model)

| # | Prompt summary | Model | Throughput (tok/s) | Quality | Delta vs small model |
|---|----------------|-------|--------------------|---------|-----------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

---

## Recommendation

<!-- Write one paragraph: which model and configuration do you recommend for Meridian's
     alert triage pipeline, and why? Cite a concrete throughput number and at least one
     qualitative quality finding. Reference the routing decision from Module 01. -->
