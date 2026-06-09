# Module 04 — Hashing, MACs & Passwords
# Standard targets: up / down / reset / demo / shell

.PHONY: up down reset demo shell

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down --rmi local --volumes --remove-orphans

demo:
	@echo "=== Module 04 — Hashing, MACs & Passwords Demo ==="
	@echo ""
	@echo "--- Part 1: SHA-256 hash cracking simulation ---"
	docker compose exec lab python3 -c "
import hashlib

# Build lookup table from wordlist
db = {}
with open('data/passwords.txt') as f:
    for line in f:
        pwd = line.strip()
        if pwd:
            db[hashlib.sha256(pwd.encode()).hexdigest()] = pwd

# Simulate hashes from a breached database
targets = {
    hashlib.sha256(b'password123').hexdigest(): 'target-1',
    hashlib.sha256(b'meridian2024').hexdigest(): 'target-2',
    hashlib.sha256(b'Tr0ub4dor&3').hexdigest(): 'target-3',
}

print('Cracking unsalted SHA-256 hashes:')
cracked = 0
for h, label in targets.items():
    result = db.get(h, None)
    if result:
        print(f'  CRACKED [{label}]: {h[:16]}... => {result}')
        cracked += 1
    else:
        print(f'  NOT FOUND [{label}]: {h[:16]}...')
print(f'Result: {cracked}/{len(targets)} cracked from wordlist')
"
	@echo ""
	@echo "--- Part 2: Argon2id password hashing (correct approach) ---"
	docker compose exec lab python3 -c "
import time
from argon2 import PasswordHasher

ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=2)
passwords = ['password123', 'meridian2024', 'Tr0ub4dor&3']

print('Argon2id hashing (each takes ~100-300ms):')
for pwd in passwords:
    start = time.perf_counter()
    h = ph.hash(pwd)
    elapsed = time.perf_counter() - start
    print(f'  Hashed in {elapsed:.3f}s: {h[:50]}...')
print()
print('At 3ms per hash: attacker can try ~333 hashes/sec')
print('At 3ms per hash vs SHA-256 (ns/hash): ~millions slower')
"
	@echo ""
	@echo "=== Run 'make shell' for the full cracking and HMAC exercises ==="

shell:
	docker compose exec lab bash
