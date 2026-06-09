"""Mock MISP API — stores events in memory."""
import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)
events: dict = {}


@app.route("/events", methods=["POST"])
def create_event():
    data = request.json.get("Event", request.json)
    eid = str(uuid.uuid4())[:8]
    data["id"] = eid
    data.setdefault("Attribute", [])
    data.setdefault("Tag", [])
    events[eid] = data
    return jsonify({"Event": data}), 201


@app.route("/attributes/add/<event_id>", methods=["POST"])
def add_attribute(event_id):
    attr = request.json.get("Attribute", request.json)
    attr["id"] = str(uuid.uuid4())[:6]
    events.setdefault(event_id, {"Attribute": [], "Tag": []})
    events[event_id]["Attribute"].append(attr)
    return jsonify({"Attribute": attr}), 201


@app.route("/tags/attachTagToObject/<event_id>/Event", methods=["POST"])
def tag_event(event_id):
    tag = request.json
    events.setdefault(event_id, {"Tag": []})
    events[event_id].setdefault("Tag", []).append(tag)
    return jsonify({"saved": True}), 200


@app.route("/events/publish/<event_id>", methods=["POST"])
def publish_event(event_id):
    if event_id in events:
        events[event_id]["published"] = True
    return jsonify({"saved": True}), 200


@app.route("/events/<event_id>", methods=["GET"])
def get_event(event_id):
    if event_id not in events:
        return jsonify({"message": "Not found"}), 404
    return jsonify({"Event": events[event_id]})


@app.route("/events/index", methods=["POST"])
def search_events():
    tag_filter = (request.json or {}).get("tag", "")
    matched = [e for e in events.values() if any(t.get("name") == tag_filter for t in e.get("Tag", []))]
    return jsonify([{"Event": e} for e in matched])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
