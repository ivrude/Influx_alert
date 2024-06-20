import sqlite3
import time
import docker


# app start container when no conection


# Параметри підключення до бази даних
db_path = 'Test_docker/Test.db'  # Змініть на ваш шлях до бази даних

# Параметри Docker
container_id = 'bef7ef2c15732be8356fadf075db869232c184383f9fd5764ab5f4ab301a8952'

# Підключення до Docker
client = docker.from_env()

def check_status():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM conection_status ORDER BY id DESC LIMIT 1")
    status = cursor.fetchone()[0]
    conn.close()
    return status

def start_container():
    container = client.containers.get(container_id)
    if container.status != 'running':
        container.start()
    return container

def stop_container(container):
    if container.status == 'running':
        container.stop()

container = None

try:
    while True:
        status = check_status()
        if status == 'trouble' and (container is None or container.status != 'running'):
            print("Status is 'trouble'. Starting container...")
            container = start_container()
        elif status == 'OK' and container is not None and container.status == 'running':
            print("Status is 'OK'. Stopping container...")
            stop_container(container)
            container = None
        time.sleep(10)  # Чекаємо 10 секунд перед наступною перевіркою
except KeyboardInterrupt:
    if container is not None and container.status == 'running':
        stop_container(container)
    print("Script interrupted. Exiting...")

