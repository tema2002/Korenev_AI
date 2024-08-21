import telebot
import config
from telebot import apihelper
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from gpt_handler import rewrite_for_kids
from keyboard_data import KEYBOARD_DATA, STYLE_PROMPTS

# Настройка прокси
PROXY = {
    'http': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASSWORD}@{config.PROXY_HOST}:{config.PROXY_PORT}',
    'https': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASSWORD}@{config.PROXY_HOST}:{config.PROXY_PORT}'
}

# Настройка использования прокси для Telegram
apihelper.proxy = PROXY

# Инициализация клиента Telegram
bot = telebot.TeleBot(config.TELEGRAM_API_KEY)

# Словарь для хранения выбора пользователя
user_choices = {}

def create_style_keyboard():
    """
    Создает клавиатуру для выбора стиля рерайта.
    """
    keyboard = InlineKeyboardMarkup()
    buttons = list(KEYBOARD_DATA.items())
    for i in range(0, len(buttons), 2):
        row = []
        for label, data in buttons[i:i+2]:
            row.append(InlineKeyboardButton(label, callback_data=data))
        keyboard.row(*row)
    keyboard.row(InlineKeyboardButton("❌ Скрыть", callback_data="hide"))
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Обработчик команд /start и /help.
    """
    bot.reply_to(message, "Привет! Выбери стиль для рерайта текста:", reply_markup=create_style_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Обработчик нажатий на кнопки клавиатуры.
    """
    if call.data == "hide":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    else:
        user_choices[call.from_user.id] = call.data
        style_name = next(key for key, value in KEYBOARD_DATA.items() if value == call.data)
        bot.answer_callback_query(call.id, f"Выбран стиль: {style_name}")
        bot.edit_message_text("Отлично! Теперь отправь мне текст для рерайта.", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """
    Обработчик всех текстовых сообщений.
    """
    user_id = message.from_user.id
    if user_id not in user_choices:
        bot.reply_to(message, "Пожалуйста, сначала выберите стиль для рерайта.", reply_markup=create_style_keyboard())
        return

    style = user_choices[user_id]
    prompt = STYLE_PROMPTS[style]
    original_text = message.text
    rewritten_text = rewrite_for_kids(original_text, prompt)
    bot.reply_to(message, rewritten_text)
    
    # Предложим выбрать новый стиль после обработки текста
    bot.send_message(message.chat.id, "Хотите выбрать другой стиль для следующего рерайта?", reply_markup=create_style_keyboard())

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling()