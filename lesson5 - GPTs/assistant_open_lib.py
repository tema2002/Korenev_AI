import os
import time
import json
from openai import OpenAI
from config import OPENAI_API_KEY, PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD

# Настройка прокси
os.environ['http_proxy'] = f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'
os.environ['https_proxy'] = f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# ID ассистента
ASSISTANT_ID = "asst_dST1Es0niOkkPgJauDeWGKWc"

def create_thread():
    return client.beta.threads.create()

def add_message_to_thread(thread_id, content):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

def run_assistant(thread_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
        model="gpt-4o"  # Используем модель GPT-4
    )
    return run

def wait_for_completion(thread_id, run_id):
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == 'completed':
            return run
        time.sleep(1)

def get_assistant_response(thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

def chat_with_assistant():
    thread = create_thread()
    print("Чат с ассистентом OpenAI. Введите 'выход' для завершения.")
    
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == 'выход':
            break
        
        add_message_to_thread(thread.id, user_input)
        run = run_assistant(thread.id)
        wait_for_completion(thread.id, run.id)
        response = get_assistant_response(thread.id)
        
        print("Ассистент:", response)

if __name__ == "__main__":
    chat_with_assistant()