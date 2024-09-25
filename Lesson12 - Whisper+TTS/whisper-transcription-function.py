import requests
import os
from config import (
    OPENAI_API_KEY, 
    PROXY_HOST, 
    PROXY_PORT, 
    PROXY_USERNAME, 
    PROXY_PASSWORD
)

def transcribe_audio(file_path, prompt="OPEN__ai"):
    url = "https://api.openai.com/v1/audio/transcriptions"
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    proxies = {
        'http': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
        'https': f'http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'
    }
    
    # Используем os.path.abspath для получения абсолютного пути
    abs_file_path = os.path.abspath(file_path)
    
    if not os.path.exists(abs_file_path):
        print(f"Файл не найден: {abs_file_path}")
        return None
    
    with open(abs_file_path, 'rb') as audio_file:
        files = {
            'file': (os.path.basename(abs_file_path), audio_file, 'audio/ogg'),
            'model': (None, 'whisper-1'),
            'prompt': (None, prompt)
        }
        
        try:
            response = requests.post(url, headers=headers, files=files, proxies=proxies)
            response.raise_for_status()  # Вызовет исключение для HTTP-ошибок
            return response.json()['text']
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
            return None

# Пример использования
if __name__ == "__main__":
    # Используем raw string для пути к файлу
    audio_file_path = r"C:\Users\lesni\Documents\_gitprojects\ai_bot_creator\Lesson12 - Whisper\audio_2024-09-24_16-58-59.ogg"
    transcript = transcribe_audio(audio_file_path)
    if transcript:
        print(f"Транскрипция: {transcript}")
    else:
        print("Не удалось получить транскрипцию.")