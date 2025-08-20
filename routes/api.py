from flask import Blueprint, jsonify
from utils.storage import load_data
from datetime import datetime

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/messages")
def api_messages():
    data = load_data()
    return jsonify({"status": "success", "total": len(data), "data": data})

@api_bp.route("/api/messages/<timestamp>")
def api_message_detail(timestamp):
    data = load_data()
    message = data.get(timestamp)
    if message:
        return jsonify({"status": "success", "data": {timestamp: message}})
    return jsonify({"status": "error", "message": "Повідомлення не знайдено"}), 404

@api_bp.route("/health")
def health_check():
    data = load_data()
    return jsonify({
        "status": "healthy",
        "timestamp": str(datetime.now()),
        "total_messages": len(data),
        "version": "1.0.0"
    })
