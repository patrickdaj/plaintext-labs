"""Simple mock threat-intel API for the enrichment pipeline lab."""
import random
from flask import Flask, jsonify

app = Flask(__name__)

VERDICTS = ["malicious", "clean", "suspicious", "unknown"]
WEIGHTS  = [0.2, 0.5, 0.15, 0.15]


@app.route("/api/v3/ip/<ip>")
def enrich_ip(ip: str):
    verdict = random.choices(VERDICTS, WEIGHTS)[0]
    return jsonify({"ioc": ip, "verdict": verdict, "abuse_score": random.randint(0, 100)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
