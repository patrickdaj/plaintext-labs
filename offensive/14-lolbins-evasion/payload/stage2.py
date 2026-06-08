#!/usr/bin/env python3
# Simulated stage-2 payload — benign for teaching purposes.
# In a real engagement this would be a reverse shell or implant.
import os, socket, datetime

print(f"[+] Stage-2 payload executed at {datetime.datetime.now().isoformat()}")
print(f"[+] PID={os.getpid()}  UID={os.getuid()}  hostname={socket.gethostname()}")
print(f"[+] /etc/passwd first line: {open('/etc/passwd').readline().strip()}")
print("[+] This is where the real implant code would run.")
