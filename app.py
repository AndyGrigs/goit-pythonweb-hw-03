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

@app.route('/api/messages')
def api_messages():
    """API для отримання всіх повідомлень у JSON форматі"""
    data = load_data()
    return jsonify(data)

@app.route('/api/messages/<timestamp>')
def api_message_detail(timestamp):
    """API для отримання конкретного повідомлення за часом"""
    data = load_data()
    message = data.get(timestamp)
    if message:
        return jsonify({timestamp: message})
    return jsonify({'error': 'Повідомлення не знайдено'}), 404

@app.route('/error.html')
@app.route('/404')
def error_404():
    """Сторінка помилки 404"""
    return render_template('error.html'), 404

@app.route('/style.css')
def serve_css():
    """Подача CSS файлу"""
    try:
        # Спочатку спробуємо static папку, потім корінь
        return send_from_directory('static', 'style.css', mimetype='text/css')
    except:
        return send_from_directory('.', 'style.css', mimetype='text/css')
    

@app.route('/logo.png')
def serve_logo():
    """Подача файлу логотипу"""
    try:
        # Спочатку спробуємо static папку, потім корінь
        return send_from_directory('static', 'logo.png', mimetype='image/png')
    except:
        return send_from_directory('.', 'logo.png', mimetype='image/png')
    
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Подача статичних файлів з папки static"""
    return send_from_directory('static', filename)

@app.errorhandler(404)
def not_found(error):
    """Обробник помилки 404"""
    return render_template('error.html'), 404

if __name__ == '__main__':
    # Створити папку templates якщо не існує
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)