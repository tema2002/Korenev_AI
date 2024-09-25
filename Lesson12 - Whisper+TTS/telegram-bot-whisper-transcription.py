import telebot
from telebot import apihelper
from config import TELEGRAM_API_KEY, OPENAI_API_KEY, PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD
import requests
import os

# Настройка прокси для telebot (если необходимо)
#apihelper.proxy = {'http': PROXY_URL, 'https': PROXY_URL}

bot = telebot.TeleBot(TELEGRAM_API_KEY)

def transcribe_audio(file_path, prompt="OPENai"):
    url = "https://api.openai.com/v1/audio/transcriptions"
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    proxies = {
        'http': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
        'https': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'
    }
    
    with open(file_path, 'rb') as audio_file:
        files = {
            'file': (os.path.basename(file_path), audio_file, 'audio/ogg'),
            'model': (None, 'whisper-1'),
            'prompt': (None, prompt)
        }
        
        try:
            response = requests.post(url, headers=headers, files=files, proxies=proxies)
            response.raise_for_status()
            return response.json()['text']
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
            return None

def text_to_speech(text):
    url = "https://api.openai.com/v1/audio/speech"
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    proxies = {
        'http': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
        'https': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'
    }
    
    data = {
        "model": "tts-1-hd",
        "input": text,
        "voice": "alloy"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, proxies=proxies)
        response.raise_for_status()
        
        # Сохраняем аудио в файл
        with open("tts_output.mp3", "wb") as f:
            f.write(response.content)
        
        return "tts_output.mp3"
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса TTS: {e}")
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может транскрибировать голосовые сообщения и озвучивать текст. Просто отправь мне голосовое сообщение, и я преобразую его в текст и обратно в речь.")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        # Получаем информацию о голосовом сообщении
        file_info = bot.get_file(message.voice.file_id)
        
        # Загружаем файл
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Сохраняем файл локально
        with open('voice_message.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Отправляем сообщение о начале обработки
        bot.reply_to(message, "Получил ваше голосовое сообщение. Начинаю транскрибацию и создание озвучки...")
        
        # Транскрибируем аудио
        transcript = transcribe_audio('voice_message.ogg')
        
        if transcript:
            bot.reply_to(message, f"Вот транскрипция вашего сообщения:\n\n{transcript}")
            
            # Создаем озвучку транскрибированного текста
            tts_file = text_to_speech(transcript)
            
            if tts_file:
                with open(tts_file, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio, caption="Озвучка транскрибированного текста")
                os.remove(tts_file)
            else:
                bot.reply_to(message, "Извините, не удалось создать озвучку текста.")
        else:
            bot.reply_to(message, "Извините, не удалось транскрибировать ваше сообщение. Попробуйте еще раз.")
        
        # Удаляем временный файл
        os.remove('voice_message.ogg')
        
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при обработке вашего голосового сообщения: {str(e)}")

if __name__ == "__main__":
    bot.polling(none_stop=True)