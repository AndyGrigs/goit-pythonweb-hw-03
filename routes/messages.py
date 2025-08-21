from flask import Blueprint, request, redirect, url_for, flash, render_template
from datetime import datetime
from utils.storage import load_data, save_data
from config import MAX_USERNAME_LENGTH, MAX_MESSAGE_LENGTH

messages_bp = Blueprint("messages", __name__)

@messages_bp.route("/message", methods=["POST"])
def handle_message():
    username = request.form.get("username", "").strip()
    message = request.form.get("message", "").strip()

    if not username:
        flash("Введіть нікнейм!", "error")
        return redirect(url_for("main.message_form"))

    if not message:
        flash("Введіть повідомлення!", "error")
        return redirect(url_for("main.message_form"))

    if len(username) > MAX_USERNAME_LENGTH or len(message) > MAX_MESSAGE_LENGTH:
        flash("Занадто довге повідомлення або нік!", "error")
        return redirect(url_for("main.message_form"))

    data = load_data()
    data[str(datetime.now())] = {"username": username, "message": message}
    save_data(data)

    flash("Повідомлення успішно відправлено!", "success")
    return redirect(url_for("main.index"))


@messages_bp.route("/read")
@messages_bp.route("/read.html")  
def read_messages():
    data = load_data()
    print(f"📖 Завантажено дані: {data}") 
    return render_template("read.html", messages=data)