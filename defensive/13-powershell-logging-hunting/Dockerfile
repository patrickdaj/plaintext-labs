# Reference lab image for Defensive Module 13 — PowerShell Logging & Hunting.
# PowerShell 7 is the analyst's tool here: we parse and hunt over bundled Script Block
# Logging (Event ID 4104) records exported from a Windows estate. No SIEM to stand up.
FROM mcr.microsoft.com/powershell:7.4-ubuntu-22.04
WORKDIR /lab
COPY . /lab
CMD ["pwsh"]
