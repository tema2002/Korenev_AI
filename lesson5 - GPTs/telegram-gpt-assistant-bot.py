import telebot
import os
import time
import httpx
from openai import OpenAI
from config import (
    TELEGRAM_API_KEY,
    OPENAI_API_KEY,
    PROXY_HOST,
    PROXY_PORT,
    PROXY_USERNAME,
    PROXY_PASSWORD,
    ASSISTANT_ID
)

# Настройка прокси для OpenAI
proxies = {
    "http://": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}",
    "https://": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
}

# Инициализация бота без прокси
bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Инициализация клиента OpenAI с прокси
client = OpenAI(
    api_key=OPENAI_API_KEY,
    http_client=httpx.Client(proxies=proxies)
)

# Словарь для хранения thread_id для каждого пользователя
user_threads = {}

def create_thread(user_id):
    """
    Создает новый поток для пользователя и сохраняет его ID.
    
    :param user_id: ID пользователя в Telegram
    :return: ID созданного потока
    """
    thread = client.beta.threads.create()
    user_threads[user_id] = thread.id
    return thread.id

def get_or_create_thread(user_id):
    """
    Получает существующий или создает новый поток для пользователя.
    
    :param user_id: ID пользователя в Telegram
    :return: ID потока пользователя
    """
    return user_threads.get(user_id) or create_thread(user_id)

def add_message_to_thread(thread_id, content):
    """
    Добавляет сообщение пользователя в поток.
    
    :param thread_id: ID потока
    :param content: Содержание сообщения
    :return: Объект сообщения
    """
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

def run_assistant(thread_id):
    """
    Запускает ассистента для обработки потока.
    
    :param thread_id: ID потока
    :return: Объект запуска
    """
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

def wait_for_completion(thread_id, run_id):
    """
    Ожидает завершения обработки запроса ассистентом.
    
    :param thread_id: ID потока
    :param run_id: ID запуска
    :return: Объект завершенного запуска
    """
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == 'completed':
            return run
        time.sleep(1)

def get_assistant_response(thread_id):
    """
    Получает ответ ассистента из потока.
    
    :param thread_id: ID потока
    :return: Текст ответа ассистента
    """
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Обработчик команд /start и /help.
    Отправляет приветственное сообщение пользователю.
    """
    bot.reply_to(message, "Привет! Я бот-ассистент шиномонтажки. Задайте мне любой вопрос, и я постараюсь на него ответить.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """
    Обработчик всех текстовых сообщений.
    Отправляет сообщение ассистенту и возвращает его ответ пользователю.
    Показывает статус 'печатает' во время обработки запроса.
    """
    user_id = message.from_user.id
    chat_id = message.chat.id
    thread_id = get_or_create_thread(user_id)
    
    # Показываем статус 'печатает'
    bot.send_chat_action(chat_id, 'typing')
    
    add_message_to_thread(thread_id, message.text)
    run = run_assistant(thread_id)
    wait_for_completion(thread_id, run.id)
    response = get_assistant_response(thread_id)
    
    # Отправляем ответ и автоматически скрываем статус 'печатает'
    bot.send_message(chat_id, response)

if __name__ == "__main__":
    bot.polling(none_stop=True)