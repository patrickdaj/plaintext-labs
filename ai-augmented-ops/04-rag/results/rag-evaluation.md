# RAG Pipeline Evaluation
## Meridian Financial — Knowledge Base Query Results

**Date:** <!-- fill in -->
**Tester:** <!-- fill in -->
**Model (generation):** <!-- e.g. tinyllama -->
**Model (embedding):** nomic-embed-text

---

## Demo query (make demo)

**Question:** What was the response procedure for the 2024 Meridian credential incident?

**Retrieved chunks (sources):**
- <!-- list the source filenames returned -->

**Generated answer:**
```
<!-- paste the answer here -->
```

**Evaluation:**
| Criterion | Pass / Fail / Partial | Notes |
|-----------|----------------------|-------|
| Chunks relevant to the question | | |
| Answer supported by retrieved chunks | | |
| Hallucination-on-context observed | | |

---

## Query 2 — Escalation path for ransomware

**Question:** What is the escalation path for a confirmed ransomware event?

**Retrieved chunks (sources):** <!-- -->

**Generated answer:**
```
```

**Evaluation:**
| Criterion | Pass / Fail / Partial | Notes |
|-----------|----------------------|-------|
| Chunks relevant | | |
| Answer grounded in chunks | | |
| Hallucination observed | | |

---

## Query 3 — PsExec detection rule

**Question:** Which detection rule covers lateral movement via PsExec?

**Retrieved chunks (sources):** <!-- -->

**Generated answer:**
```
```

**Evaluation:** <!-- -->

---

## Query 4 — Log retention

**Question:** How long does Meridian retain network flow logs?

**Retrieved chunks (sources):** <!-- -->

**Generated answer:**
```
```

**Evaluation:** <!-- -->

---

## Out-of-corpus query — Cryptocurrency payments

**Question:** What is Meridian's policy on cryptocurrency payments?

**Retrieved chunks (sources):** <!-- Were irrelevant chunks returned, or none? -->

**Generated answer:**
```
```

**Behaviour observed:** <!-- Did the model say "I don't have enough information"? Did it hallucinate a policy? -->

---

## New document retrieval

**Document added:** <!-- filename -->
**Query used:** <!-- what did you ask? -->
**Retrieved:** Yes / No
**Notes:** <!-- -->
