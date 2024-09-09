#Телеграм + ассистент
import telebot
import config
from telebot import apihelper
from openai import OpenAI
import time
import os
import httpx
import threading
import re

# Настройка прокси
PROXY = {
    'http://': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASSWORD}@{config.PROXY_HOST}:{config.PROXY_PORT}',
    'https://': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASSWORD}@{config.PROXY_HOST}:{config.PROXY_PORT}'
}

# Настройка использования прокси для Telegram
apihelper.proxy = PROXY

# Настройка прокси для OpenAI через переменные окружения
os.environ['http_proxy'] = PROXY['http://']
os.environ['https_proxy'] = PROXY['https://']

# Инициализация клиента Telegram
bot = telebot.TeleBot(config.TELEGRAM_API_KEY)

# Создание HTTP клиента с прокси
http_client = httpx.Client(proxies=PROXY)

# Инициализация клиента OpenAI с учетом прокси
openai_client = OpenAI(
    api_key=config.OPENAI_API_KEY,
    http_client=http_client
)

# ID ассистента
ASSISTANT_ID = "asst_dST1Es0niOkkPgJauDeWGKWc"

# Словарь для хранения потоков пользователей
user_threads = {}

def create_thread():
    return openai_client.beta.threads.create()

def add_message_to_thread(thread_id, content):
    return openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

def run_assistant(thread_id):
    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
        model="gpt-4o"
    )
    return run

def send_typing_action(chat_id):
    bot.send_chat_action(chat_id, 'typing')

def wait_for_completion(thread_id, run_id, chat_id):
    typing_thread = threading.Thread(target=lambda: send_typing_action(chat_id))
    typing_thread.start()
    
    while True:
        run = openai_client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == 'completed':
            break
        time.sleep(4)  # Проверяем каждые 4 секунды
        send_typing_action(chat_id)  # Обновляем статус "печатает"
    
    typing_thread.join(timeout=1)  # Ждем завершения потока не более 1 секунды

def clean_text(text):
    """
    Удаляет ссылки вида 【6:0†source】 из текста.
    """
    return re.sub(r'【\d+:\d+†[^】]+】', '', text)

def get_assistant_response(thread_id):
    messages = openai_client.beta.threads.messages.list(thread_id=thread_id)
    raw_response = messages.data[0].content[0].text.value
    return clean_text(raw_response)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Обработчик команд /start и /help.
    """
    bot.reply_to(message, "Привет! Я бот мастерской АвтоШина. Чем могу помочь?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """
    Обработчик всех текстовых сообщений.
    """
    user_id = message.from_user.id
    if user_id not in user_threads:
        user_threads[user_id] = create_thread().id

    thread_id = user_threads[user_id]
    
    # Отправляем статус "печатает"
    send_typing_action(message.chat.id)
    
    add_message_to_thread(thread_id, message.text)
    run = run_assistant(thread_id)
    wait_for_completion(thread_id, run.id, message.chat.id)
    response = get_assistant_response(thread_id)
    
    # Отправляем очищенный ответ
    bot.reply_to(message, response)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()