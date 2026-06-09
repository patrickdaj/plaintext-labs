"""
Mock threat-intel API — mimics VirusTotal/AbuseIPDB response shapes.
Returns realistic verdicts for specific IOCs; 429 once for two IOCs to test retry logic.
"""

from flask import Flask, jsonify, request
import time

app = Flask(__name__)

# Track 429 retries
_retry_counts: dict[str, int] = {}

IP_DATA = {
    "185.220.101.1": {"verdict": "malicious", "abuse_score": 95, "asn": "AS4444", "country": "RU", "reports": 142},
    "198.51.100.77": {"verdict": "malicious", "abuse_score": 87, "asn": "AS12345", "country": "CN", "reports": 89},
    "8.8.8.8":       {"verdict": "clean",     "abuse_score": 0,  "asn": "AS15169 Google", "country": "US", "reports": 0},
    "1.1.1.1":       {"verdict": "clean",     "abuse_score": 0,  "asn": "AS13335 Cloudflare", "country": "AU", "reports": 0},
    "203.0.113.10":  {"verdict": "suspicious","abuse_score": 45, "asn": "AS9876", "country": "BR", "reports": 12},
    "10.0.1.50":     {"verdict": "clean",     "abuse_score": 0,  "asn": "RFC1918", "country": "private", "reports": 0},
    "172.16.0.5":    {"verdict": "clean",     "abuse_score": 0,  "asn": "RFC1918", "country": "private", "reports": 0},
    # These two return 429 on the first call
    "192.168.100.200": {"verdict": "malicious", "abuse_score": 99, "asn": "AS99999", "country": "XX", "reports": 300},
    "198.18.0.9":      {"verdict": "suspicious","abuse_score": 50, "asn": "AS55555", "country": "DE", "reports": 8},
}

HASH_DATA = {
    "44d88612fea8a8f36de82e1278abb02f": {"verdict": "malicious", "family": "Emotet",   "engines_flagged": 62, "total_engines": 72},
    "e3b0c44298fc1c149afbf4c8996fb924": {"verdict": "clean",     "family": None,        "engines_flagged": 0,  "total_engines": 72},
    "d8e8fca2dc0f896fd7cb4cb0031ba249": {"verdict": "malicious", "family": "Cobalt Strike", "engines_flagged": 55, "total_engines": 72},
    "aabbccddeeff00112233445566778899": {"verdict": "suspicious","family": None,        "engines_flagged": 3,  "total_engines": 72},
}


@app.route("/api/v3/ip/<ip>")
def enrich_ip(ip: str):
    # Simulate rate limiting for specific IPs on first call
    if ip in ("192.168.100.200", "198.18.0.9"):
        key = f"ip:{ip}"
        count = _retry_counts.get(key, 0)
        if count == 0:
            _retry_counts[key] = 1
            return jsonify({"error": "rate limited"}), 429

    if ip not in IP_DATA:
        return jsonify({"error": "not found"}), 404

    data = IP_DATA[ip]
    return jsonify({"ioc": ip, "type": "ip", **data})


@app.route("/api/v3/hash/<hash_value>")
def enrich_hash(hash_value: str):
    if hash_value not in HASH_DATA:
        return jsonify({"error": "not found"}), 404

    data = HASH_DATA[hash_value]
    return jsonify({"ioc": hash_value, "type": "hash", **data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
