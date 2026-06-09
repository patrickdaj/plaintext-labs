# Reference lab image for Offensive Module 15 — PowerShell Offensive Tradecraft.
# PowerShell 7 on Linux: enough to build and run real cradles, encoded commands,
# and obfuscation — the cross-platform engine behaves like the Windows one for the
# language-level tradecraft this lab teaches. (AMSI is a Windows runtime feature;
# the lab documents the Windows-VM path for that part.)
FROM mcr.microsoft.com/powershell:7.4-ubuntu-22.04
WORKDIR /lab
COPY . /lab
CMD ["pwsh"]
