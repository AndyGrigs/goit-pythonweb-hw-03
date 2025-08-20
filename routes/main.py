from flask import Blueprint, render_template, redirect, url_for, flash
import json
import os

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")




@main_bp.route("/message.html")
def message_form():
    try:
        return render_template("message.html")
    except:
        flash("Помилка завантаження форми", "error")
        return redirect(url_for("main.index"))

@main_bp.route("/error.html")
def error_page():
    return render_template("error.html"), 404

@main_bp.route("/read.html")
def read_messages():
    data_file = os.path.join(os.path.dirname(__file__), "..", "data.json")
    messages = []
    try:
        with open(data_file, encoding="utf-8") as f:
            messages = json.load(f)
    except Exception:
        flash("Не вдалося завантажити повідомлення", "error")
    return render_template("read.html", messages=messages)