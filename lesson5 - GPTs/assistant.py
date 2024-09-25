import requests
import json
import time
from config import TELEGRAM_API_KEY, OPENAI_API_KEY, PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD, ASSISTANT_ID

# Настройки
API_BASE = "https://api.openai.com/v1"

# Настройки прокси
PROXIES = {
    "http": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}",
    "https": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
}

# Заголовки для запросов
HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
    "OpenAI-Beta": "assistants=v2"  # Обновлено для использования v2 API
}

def create_thread():
    """Создает новый тред для общения."""
    url = f"{API_BASE}/threads"
    response = requests.post(url, headers=HEADERS, proxies=PROXIES)
    return response.json()['id']

def add_message_to_thread(thread_id, content):
    """Добавляет сообщение в тред."""
    url = f"{API_BASE}/threads/{thread_id}/messages"
    payload = json.dumps({
        "role": "user",
        "content": content
    })
    response = requests.post(url, headers=HEADERS, data=payload, proxies=PROXIES)
    return response.json()

def create_run(thread_id):
    """Создает запуск для обработки сообщения ассистентом."""
    url = f"{API_BASE}/threads/{thread_id}/runs"
    payload = json.dumps({
        "assistant_id": ASSISTANT_ID
    })
    response = requests.post(url, headers=HEADERS, data=payload, proxies=PROXIES)
    return response.json()

def get_run_status(thread_id, run_id):
    """Получает статус запуска."""
    url = f"{API_BASE}/threads/{thread_id}/runs/{run_id}"
    response = requests.get(url, headers=HEADERS, proxies=PROXIES)
    return response.json()

def get_messages(thread_id):
    """Получает сообщения из треда."""
    url = f"{API_BASE}/threads/{thread_id}/messages"
    response = requests.get(url, headers=HEADERS, proxies=PROXIES)
    return response.json()['data']

def chat_with_assistant():
    print("Чат с ассистентом OpenAI (v2 API). Для выхода введите 'exit'.")
    thread_id = create_thread()
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == 'exit':
            break

        # Добавляем сообщение в тред
        add_message_to_thread(thread_id, user_input)

        # Создаем запуск
        run = create_run(thread_id)
        run_id = run['id']

        # Ожидаем завершения запуска
        while True:
            status = get_run_status(thread_id, run_id)
            if status['status'] == 'completed':
                break
            elif status['status'] in ['failed', 'cancelled', 'expired']:
                print(f"Ошибка: Запуск завершился со статусом {status['status']}")
                return
            time.sleep(1)  # Небольшая задержка перед следующей проверкой

        # Получаем последнее сообщение ассистента
        messages = get_messages(thread_id)
        assistant_message = next((msg for msg in messages if msg['role'] == 'assistant'), None)
        if assistant_message:
            print("Ассистент:", assistant_message['content'][0]['text']['value'])
        else:
            print("Ассистент: Извините, не удалось получить ответ.")

if __name__ == "__main__":
    chat_with_assistant()