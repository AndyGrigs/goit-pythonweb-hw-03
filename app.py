from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory, flash
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'storage/data.json'

def load_data():
    """Завантажити дані з JSON файлу"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except:
        return {}
    
def save_data(data):
    """Зберегти дані в JSON файл"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template('index.hhtml')

@app.route('/message.html')
@app.route('/message', methods=['POST'])
def handle_message():
    """Обробка відправленого повідомлення"""
    username = request.form.get('username', '').strip()
    message = request.form.get('message', '').strip()
    
    
    # Валідація даних
    if not username:
        flash('Будь ласка, введіть ваш нікнейм!', 'error')
        return redirect(url_for('message_form'))
    
    if not message:
        flash('Будь ласка, введіть повідомлення!', 'error')
        return redirect(url_for('message_form'))
    
    if len(username) > 50:
        flash('Нікнейм занадто довгий (максимум 50 символів)!', 'error')
        return redirect(url_for('message_form'))
    
    if len(message) > 500:
        flash('Повідомлення занадто довге (максимум 500 символів)!', 'error')
        return redirect(url_for('message_form'))
    
    try:
        # Завантажити існуючі дані
        data = load_data()
        
        # Створити ключ з поточного часу
        timestamp_key = str(datetime.now())
        
        # Створити словник для нового повідомлення
        message_dict = {
            'username': username,  
            'message': message     
        }
        
        # Додати повідомлення з часовим ключем
        data[timestamp_key] = message_dict
        
        # Зберегти дані
        save_data(data)
        
        flash('Повідомлення успішно відправлено!', 'success')
        
    except Exception as e:
        flash('Помилка при збереженні повідомлення. Спробуйте ще раз.', 'error')
        print(f"Помилка збереження: {e}")
    
    # Перенаправити на головну сторінку
    return redirect(url_for('index'))

@app.reute('/read')
def read_messages():
    """Сторінка для читання всіх повідомлень"""
    data = load_data()
    return render_template('read.html', messages=data)