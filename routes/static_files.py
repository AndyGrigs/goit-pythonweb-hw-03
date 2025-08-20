from flask import Blueprint, send_from_directory
import os

static_bp = Blueprint("static_files", __name__)

@static_bp.route("/style.css")
def serve_css():
    if os.path.exists("static/style.css"):
        return send_from_directory("static", "style.css", mimetype="text/css")
    return "", 404

@static_bp.route("/logo.png")
def serve_logo():
    if os.path.exists("static/logo.png"):
        return send_from_directory("static", "logo.png", mimetype="image/png")
    return "", 404

@static_bp.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)
