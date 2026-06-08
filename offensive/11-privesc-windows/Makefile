.PHONY: demo triage

# 'make demo' runs the triage tool against sample winPEAS output.
# The Windows-side steps (plant-misconfigs.ps1, winPEAS.exe) require a Windows VM.
demo:
	python3 triage.py

# Run triage against a real winPEAS output file:
#   make triage FILE=winpeas_out.txt
triage:
	python3 triage.py $(FILE)
