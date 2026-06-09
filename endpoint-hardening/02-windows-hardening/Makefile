# Module 02 — Windows Hardening to CIS
# The hardening itself runs on a Windows VM (see lab.md).
# The scoring script runs on any platform with Python 3.
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

BEFORE ?= data/sample-cis-report-before.json
AFTER  ?= data/sample-cis-report-after.json

up:
	@echo "Module 02: Windows hardening runs on a Windows 11 VM."
	@echo "See lab.md for the VM setup instructions."
	@echo "The scoring demo (make demo) runs on any platform."

down:
	@echo "Nothing to stop."

reset:
	@echo "Nothing to reset."

demo:
	@echo "=== CIS-CAT Lite — Before/After Scoring Demo ==="
	@echo ""
	python3 score_report.py $(BEFORE) $(AFTER)
	@echo ""
	@echo "=== To use your own reports from the Windows VM: ==="
	@echo "  make demo BEFORE=path/to/cis-report-before.json AFTER=path/to/cis-report-after.json"
	@echo ""
	@echo "=== Threshold check (exit 1 if score < 70): ==="
	python3 score_report.py $(BEFORE) $(AFTER) --min-score 70; \
	  echo "Exit code: $$?"

shell:
	@echo "No container for this module. Use your Windows VM."
