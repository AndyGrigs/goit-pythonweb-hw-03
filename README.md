Для запуску додатка з Docker у вас вже є всі необхідні файли. Ось детальна інструкція:

## 🐳 Методи запуску

### **Метод 1: Docker Compose (найпростіший)**

```bash
# 1. Переконайтеся що ви в директорії проекту
cd your-project-directory

# 2. Зібрати та запустити
docker-compose up --build

# Або у фоновому режимі
docker-compose up --build -d
```

### **Метод 2: Звичайні Docker команди**

```bash
# 1. Створити папку для даних (важливо!)
mkdir -p storage

# 2. Зібрати Docker образ
docker build -t python-courses-app .

# 3. Запустити контейнер з volume
docker run -d \
  --name python-courses \
  -p 3000:3000 \
  -v "$(pwd)/storage:/app/storage" \
  python-courses-app
```

### **Крок 3: Запуск через Docker Compose**

**Виконайте в терміналі:**
```bash
# Запуск з логами
docker-compose up --build

# Або у фоні
docker-compose up --build -d

# Переглянути логи
docker-compose logs -f
```

### **Крок 4: Перевірка роботи**

Відкрийте браузер та перейдіть на:
- **Головна**: http://localhost:3000/
- **Форма**: http://localhost:3000/message.html
- **API**: http://localhost:3000/api/messages
- **Health**: http://localhost:3000/health

## 🔧 Корисні Docker команди:

### **Управління контейнером:**
```bash
# Зупинити
docker-compose down

# Перезапустити
docker-compose restart

# Переглянути статус
docker-compose ps

# Логи в реальному часі
docker-compose logs -f python-courses-app
```

### **Налагодження:**
```bash
# Підключитися до контейнера
docker exec -it python-courses /bin/bash

# Перевірити файли в контейнері
docker exec python-courses ls -la /app

# Перевірити volume
docker exec python-courses ls -la /app/storage
```

### **Очищення:**
```bash
# Зупинити та видалити контейнери
docker-compose down

# Видалити образи
docker rmi python-courses-app

# Повне очищення
docker system prune -a
```

## 🔍 Вирішення проблем:

### **Проблема: Порт зайнятий**
```bash
# Знайти процес на порту 3000
lsof -i :3000                # Linux/Mac
netstat -ano | findstr :3000 # Windows

# Змінити порт у docker-compose.yml
ports:
  - "3001:3000"  # Використати порт 3001
```

### **Проблема: Файли не знайдені**
```bash
# Перевірити структуру
ls -la
tree .  # якщо встановлено

# Перевірити .dockerignore
cat .dockerignore
```

### **Проблема: Volume не працює**
```bash
# Перевірити монтування
docker inspect python-courses | grep -A 10 "Mounts"

# Створити папку вручну
mkdir -p ./storage
chmod 755 ./storage
```

## 📊 Моніторинг роботи:

### **Перевірити логи:**
```bash
# Логи Docker Compose
docker-compose logs

# Логи конкретного сервісу
docker-compose logs python-courses-app

# Останні 50 рядків
docker-compose logs --tail=50 python-courses-app
```

### **Перевірити ресурси:**
```bash
# Статистика контейнера
docker stats python-courses

# Процеси в контейнері
docker exec python-courses ps aux
```

## 🎯 Тестування після запуску:

1. **Перевірте статус:**
   ```bash
   curl http://localhost:3000/health
   ```

2. **Відправте тестове повідомлення:**
   ```bash
   curl -X POST http://localhost:3000/message \
     -d "username=DockerTest&message=Hello from Docker!"
   ```

3. **Перевірте збереження:**
   ```bash
   cat ./storage/data.json
   ```

4. **Перевірте API:**
   ```bash
   curl http://localhost:3000/api/messages
   ```
