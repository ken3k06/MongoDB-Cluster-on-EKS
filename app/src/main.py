import os
from datetime import datetime, timezone

from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://admin:admin123@localhost:27017/?authSource=admin",
)
MONGO_DB = os.getenv("MONGO_DB", "nt132_app")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "items")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
database = client[MONGO_DB]
items_collection = database[MONGO_COLLECTION]

app = Flask(__name__)


def serialize_item(document: dict) -> dict:
    return {
        "id": str(document.get("_id")),
        "name": document.get("name"),
        "value": document.get("value"),
        "created_at": document.get("created_at"),
    }


@app.get("/")
def root():
    return jsonify(
        {
            "service": "nt132-sample-app",
            "status": "ok",
            "time": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/health")
def health():
    try:
        client.admin.command("ping")
        return jsonify({"status": "healthy", "mongo": "up"}), 200
    except PyMongoError as error:
        return jsonify({"status": "unhealthy", "mongo": str(error)}), 503


@app.post("/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")

    if not name or not isinstance(name, str):
        return jsonify({"error": "field 'name' is required and must be a string"}), 400

    item = {
        "name": name,
        "value": payload.get("value"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    result = items_collection.insert_one(item)
    created_item = items_collection.find_one({"_id": result.inserted_id})
    return jsonify(serialize_item(created_item)), 201


@app.get("/items")
def list_items():
    limit_raw = request.args.get("limit", "20")
    try:
        limit = max(1, min(int(limit_raw), 100))
    except ValueError:
        return jsonify({"error": "'limit' must be an integer"}), 400

    cursor = items_collection.find().sort("_id", -1).limit(limit)
    return jsonify([serialize_item(item) for item in cursor]), 200


@app.get("/items/<item_id>")
def get_item(item_id: str):
    try:
        oid = ObjectId(item_id)
    except Exception:
        return jsonify({"error": "invalid item id"}), 400

    item = items_collection.find_one({"_id": oid})
    if not item:
        return jsonify({"error": "item not found"}), 404

    return jsonify(serialize_item(item)), 200


@app.delete("/items/<item_id>")
def delete_item(item_id: str):
    try:
        oid = ObjectId(item_id)
    except Exception:
        return jsonify({"error": "invalid item id"}), 400

    result = items_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return jsonify({"error": "item not found"}), 404

    return jsonify({"deleted": True, "id": item_id}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
