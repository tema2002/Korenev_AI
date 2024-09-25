import telebot
from config import TELEGRAM_API_KEY
from gpt_handler import rewrite_for_kids

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Обработчик команд /start и /help.
    Отправляет приветственное сообщение пользователю.
    """
    bot.reply_to(message, "Привет! Я бот, который может переписать любой текст для детей 10 лет. Просто отправь мне текст, и я сделаю его понятным и интересным для детей!")

@bot.message_handler(func=lambda message: True)
def rewrite_text(message):
    """
    Обработчик всех текстовых сообщений.
    Отправляет текст на переписывание и возвращает результат пользователю.
    """
    original_text = message.text
    bot.reply_to(message, "Перерабатываю ваш текст... Это может занять некоторое время.")
    
    rewritten_text = rewrite_for_kids(original_text)
    bot.reply_to(message, f"Вот переписанный текст для детей 10 лет:\n\n{rewritten_text}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
