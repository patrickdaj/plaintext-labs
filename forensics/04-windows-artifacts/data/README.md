# Module 04 — Data Directory

## security-events.jsonl
Pre-shaped Windows Security event records in JSON format. These represent events from
`MERIDIAN-FIN-WS01.meridian.internal` during the incident window (2024-03-15 02:09–02:31 UTC).

The demo script parses this file directly. In a real investigation, you would use:
- `chainsaw hunt /path/to/Security.evtx --sigma ...` against a real EVTX file
- Real EVTX samples: https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES

To use real EVTX files with this lab: place them in this directory and update the
docker-compose.yml volume mount or `make demo` command to point at your EVTX.

## ntuser-parsed.json
Pre-parsed synthetic registry hive representing `NTUSER.DAT` from the compromised
finance account. In a real investigation, use `python-registry` against a real hive:
```python
from Registry import Registry
reg = Registry.Registry('NTUSER.DAT')
```
Real training hives are available from:
- https://github.com/EricZimmermanTrainingFiles (free training datasets)
