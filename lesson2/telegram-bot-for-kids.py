import telebot
import config
from telebot import apihelper
from gpt_handler import rewrite_for_kids

# Настройка прокси
PROXY = {
    'http': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASSWORD}@{config.PROXY_HOST}:{config.PROXY_PORT}',
    'https': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASSWORD}@{config.PROXY_HOST}:{config.PROXY_PORT}'
}

# Настройка использования прокси для Telegram
apihelper.proxy = PROXY

# Инициализация клиента Telegram
bot = telebot.TeleBot(config.TELEGRAM_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Обработчик команд /start и /help.
    """
    bot.reply_to(message, "Привет! Отправь мне текст, и я перепишу его так, чтобы он был понятен детям 10 лет.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """
    Обработчик всех текстовых сообщений.
    """
    original_text = message.text
    rewritten_text = rewrite_for_kids(original_text)
    bot.reply_to(message, rewritten_text)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()
