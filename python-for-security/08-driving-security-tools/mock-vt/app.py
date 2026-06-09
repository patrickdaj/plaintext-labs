"""Mock VirusTotal API."""
from flask import Flask, jsonify

app = Flask(__name__)

IP_DATA = {
    "185.220.101.1": {"last_analysis_stats": {"malicious": 62, "suspicious": 3, "harmless": 0}, "reputation": -95},
    "198.51.100.77":  {"last_analysis_stats": {"malicious": 55, "suspicious": 2, "harmless": 1}, "reputation": -87},
    "8.8.8.8":        {"last_analysis_stats": {"malicious": 0,  "suspicious": 0, "harmless": 72}, "reputation": 10},
}
HASH_DATA = {
    "44d88612fea8a8f36de82e1278abb02f": {"last_analysis_stats": {"malicious": 62, "suspicious": 0}, "meaningful_name": "Emotet"},
    "e3b0c44298fc1c149afbf4c8996fb924": {"last_analysis_stats": {"malicious": 0, "suspicious": 0}, "meaningful_name": None},
}


@app.route("/api/v3/ip_addresses/<ip>")
def vt_ip(ip):
    if ip not in IP_DATA:
        return jsonify({"error": {"code": "NotFoundError"}}), 404
    return jsonify({"data": {"attributes": IP_DATA[ip]}})


@app.route("/api/v3/files/<hash_value>")
def vt_hash(hash_value):
    if hash_value not in HASH_DATA:
        return jsonify({"error": {"code": "NotFoundError"}}), 404
    return jsonify({"data": {"attributes": HASH_DATA[hash_value]}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
