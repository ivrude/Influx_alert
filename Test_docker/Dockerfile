# Використовуємо базовий образ Python
FROM python:3.9

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл requirements.txt у робочу директорію
COPY requirements.txt /app/

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли додатку у робочу директорію
COPY . /app

# Відкриваємо порт 5000 для Flask додатку
EXPOSE 5000

# Команда для запуску Flask додатку
CMD ["python", "app.py"]
