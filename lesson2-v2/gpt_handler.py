import requests
from config import OPENAI_API_KEY, GPT_MODEL, OPENAI_API_URL, PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD

def rewrite_for_kids(text):
    """
    Функция для отправки запроса к GPT API и получения переписанного текста для детей 10 лет.
    
    :param text: Исходный текст для переписывания
    :return: Переписанный текст, понятный детям 10 лет
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": GPT_MODEL,
        "messages": [
            {"role": "system", "content": "Ты - эксперт по переписыванию текстов для детей 10 лет. Твоя задача - переписать предоставленный текст так, чтобы он был понятен и интересен детям этого возраста."},
            {"role": "user", "content": f"Перепиши следующий текст для детей 10 лет: {text}"}
        ]
    }
    
    proxies = {
        "http": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}",
        "https": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
    }
    
    try:
        response = requests.post(OPENAI_API_URL, json=data, headers=headers, proxies=proxies)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Произошла ошибка при обращении к GPT API: {str(e)}"