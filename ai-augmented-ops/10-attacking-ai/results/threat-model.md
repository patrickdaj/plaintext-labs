# Threat Model — Meridian SoC Copilot
## AI Security Assessment

**Date:** <!-- fill in -->
**System:** Meridian SoC Copilot — Ollama (tinyllama) + ChromaDB RAG + MCP tools

---

## Adversaries

| Adversary | Motivation | Access level | Likely technique |
|-----------|-----------|--------------|-----------------|
| External attacker (alert injection) | Reclassify high-severity alerts as low to avoid detection | Indirect — via malicious endpoint sending alerts | Prompt injection via alert text (ATLAS AML.T0051) |
| Insider threat (corpus poisoning) | Manipulate analyst response recommendations | Direct — write access to knowledge base ingestion | Corpus poisoning (ATLAS AML.T0016) |
| Sophisticated attacker (combined) | Persistent access to Meridian environment | Indirect, persistent | Combined corpus poisoning + prompt injection |

---

## Assets

| Asset | Value to attacker |
|-------|-----------------|
| Alert severity classifications | Reclassify CRITICAL to LOW → avoid containment |
| System prompt content | Understand instructions → craft targeted injections |
| Knowledge base contents | Exfiltrate internal runbooks and incident data |
| MCP tool capabilities | Abuse tool calls for lateral movement or recon |

---

## Attack surface

| Surface | Threat | Untrusted input? |
|---------|--------|----------------|
| Alert text (description, title) | Prompt injection | Yes — comes from endpoints/EDR |
| Tool results (threat intel, alerts) | Tool output poisoning | Yes — data from external or manipulated stores |
| RAG retrieved chunks | Corpus poisoning | Yes — if ingestion pipeline is not access-controlled |
| Model API | Direct probing, jailbreak | Yes — if API is exposed beyond localhost |
| MCP tool arguments | Tool abuse via oversized/malicious input | Yes — model-generated |

---

## Top 3 threats

### Threat 1 — Severity Manipulation via Alert Injection
**OWASP:** LLM01 — Prompt Injection
**MITRE ATLAS:** AML.T0051 — LLM Prompt Injection
**Likelihood:** HIGH — alert data is inherently untrusted
**Impact:** CRITICAL — missed alert → undetected breach
**Mitigations implemented:** Input sanitisation (Module 09), severity output validation
**Residual risk:** <!-- describe what still works after mitigation -->

### Threat 2 — Runbook Corruption via Corpus Poisoning
**OWASP:** LLM09 — Overreliance
**MITRE ATLAS:** AML.T0016 — Obtain Capabilities
**Likelihood:** MEDIUM — requires write access to ingestion pipeline
**Impact:** HIGH — analyst follows poisoned guidance during incident
**Mitigations implemented:** Output URL validation (Module 09), corpus access control
**Residual risk:** <!-- describe what still works after mitigation -->

### Threat 3 — System Prompt Extraction via Leakage
**OWASP:** LLM02 — Insecure Output Handling
**MITRE ATLAS:** AML.T0054 — LLM Jailbreak
**Likelihood:** MEDIUM — requires attacker to interact with the copilot API
**Impact:** MEDIUM — knowledge of system prompt enables more targeted injections
**Mitigations implemented:** Model-level resistance (tested by garak/promptfoo)
**Residual risk:** <!-- describe what still works after mitigation -->

---

## Mitigations implemented

| Mitigation | Module | Coverage |
|-----------|--------|---------|
| Input sanitisation (strip injection patterns) | 09 | Prompt injection via alert text |
| Output URL validation | 09 | Corpus poisoning via malicious runbook |
| MCP tool input validation | 05 | Tool abuse via oversized input |
| Corpus ingestion access control | 09 | Corpus poisoning |

---

## Residual risk summary

<!-- One paragraph: after all implemented mitigations, what threats remain open?
     What would be required to close them? What is the acceptable risk threshold
     for production deployment of this copilot? -->
