from flask import Blueprint, jsonify, request
from flask import render_template
from app.extensions import mongo
import uuid
from datetime import datetime
from app.webhook.utils import parse_github_timestamp

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    data = None

    # PUSH EVENT
    if event_type == "push":
        data = {
            "id": str(uuid.uuid4()),
            "request_id": payload.get("after"),
            "author": payload["pusher"]["name"],
            "action": "push",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": parse_github_timestamp(payload["head_commit"]["timestamp"])
        }

    # PULL REQUEST & MERGE EVENTS
    elif event_type == "pull_request":
        pr = payload["pull_request"]

        # Pull Request Opened
        if payload["action"] == "opened":
            data = {
                "id": str(uuid.uuid4()),
                "request_id": str(pr["id"]),
                "author": pr["user"]["login"],
                "action": "pull_request",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": parse_github_timestamp(pr["created_at"])
            }

        # Pull Request Merged
        elif payload["action"] == "closed" and pr["merged"]:
            data = {
                "id": str(uuid.uuid4()),
                "request_id": str(pr["id"]),
                "author": pr["merged_by"]["login"],
                "action": "merge",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": parse_github_timestamp(pr["merged_at"])
            }

    # Store event if valid
    if data:
        try:
            mongo.db.events.insert_one(data)
        except Exception as e:
            print(f"Error inserting data into MongoDB: {e}")
            return jsonify({"status": "error", "message": "Database error"}), 500

    return jsonify({"status": "received"}), 200


@webhook.route('/events', methods=["GET"])
def get_events():

    events = list(
        mongo.db.events.find({}, {"_id": 0}).sort("timestamp", -1)
    )
    # Convert datetime to ISO string for frontend
    for event in events:
        if isinstance(event.get("timestamp"), datetime):
            event["timestamp"] = event["timestamp"].isoformat()

    return jsonify(events), 200

@webhook.route("/", methods=["GET"])
def index():
    return render_template("index.html")

