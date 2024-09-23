import telebot
import config
from telebot import apihelper
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from gpt_image_analysis import analyze_image

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
    bot.reply_to(message, "Привет! Отправь мне изображение, и я проанализирую его содержимое.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """
    Обработчик для полученных фотографий.
    """
    try:
        # Получаем информацию о фото
        file_info = bot.get_file(message.photo[-1].file_id)
        
        # Загружаем фото
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Сохраняем фото локально
        src = 'temp_image.jpg'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Анализируем изображение
        analysis_result = analyze_image(src, is_url=False)
        
        # Отправляем результат анализа
        bot.reply_to(message, f"Анализ изображения:\n\n{analysis_result}")
    
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при обработке изображения: {str(e)}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """
    Обработчик всех остальных сообщений.
    """
    bot.reply_to(message, "Пожалуйста, отправьте изображение для анализа.")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()
