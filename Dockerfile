# Використовуємо офіційний Python образ
FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл з залежностями
COPY requirements.txt .

# Встановлюємо Python залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код додатка
COPY . .

# Створюємо директорії для templates та storage
RUN mkdir -p templates storage static

# Переміщуємо HTML файли в templates (якщо вони не там)
RUN if [ -f index.html ]; then mv index.html templates/; fi && \
    if [ -f message.html ]; then mv message.html templates/; fi && \
    if [ -f error.html ]; then mv error.html templates/; fi

# Переміщуємо статичні файли
RUN if [ -f style.css ]; then mv style.css static/ || cp style.css static/; fi && \
    if [ -f logo.png ]; then mv logo.png static/ || cp logo.png static/; fi

# Створюємо том для збереження даних
VOLUME ["/app/storage"]

# Відкриваємо порт 3000
EXPOSE 3000

# Створюємо непривілейованого користувача для безпеки
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Команда для запуску додатка
CMD ["python", "app.py"]