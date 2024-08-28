import openai
import config
import base64
import os
import requests
from io import BytesIO
from PIL import Image

# Настройка OpenAI для использования прокси
openai.api_key = config.OPENAI_API_KEY
openai.proxy = {
    'http': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASSWORD}@{config.PROXY_HOST}:{config.PROXY_PORT}',
    'https': f'http://{config.PROXY_USERNAME}:{config.PROXY_PASSWORD}@{config.PROXY_HOST}:{config.PROXY_PORT}'
}

def rewrite_for_kids(text, prompt):
    """
    Функция для рерайта текста с использованием заданного промпта.
    
    Args:
    text (str): Исходный текст для рерайта.
    prompt (str): Промпт для настройки поведения GPT.
    
    Returns:
    str: Переписанный текст.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Адаптируй этот текст: {text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка при использовании GPT: {e}")
        return "Извините, произошла ошибка при обработке текста."

def generate_image_prompt(text):
    """
    Функция для генерации короткого промпта для Stable Diffusion на основе отрерайченного текста.
    
    Args:
    text (str): Отрерайченный текст.
    
    Returns:
    str: Короткий промпт для генерации изображения.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты - эксперт по созданию промптов для генерации изображений. Твоя задача - создать краткий, но описательный промпт для Stable Diffusion на основе предоставленного текста. Промпт должен быть на английском языке и не превышать 30-40 слов."},
                {"role": "user", "content": f"Создай короткий промпт для генерации изображения на основе этого текста: {text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка при генерации промпта для изображения: {e}")
        return "A simple, colorful illustration"

def generate_image(prompt, api_key, engine_id="stable-diffusion-v1-6", width=1024, height=1024):
    """
    Функция для генерации изображения с использованием Stability AI API.
    
    Args:
    prompt (str): Текстовый промпт для генерации изображения.
    api_key (str): API ключ для Stability AI.
    engine_id (str): ID модели для генерации изображения.
    width (int): Ширина генерируемого изображения.
    height (int): Высота генерируемого изображения.
    
    Returns:
    PIL.Image: Сгенерированное изображение.
    """
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    image_data = base64.b64decode(data["artifacts"][0]["base64"])
    image = Image.open(BytesIO(image_data))
    return image

def process_text_and_generate_image(text, rewrite_prompt, api_key):
    """
    Функция для обработки текста и генерации изображения.
    
    Args:
    text (str): Исходный текст.
    rewrite_prompt (str): Промпт для рерайта текста.
    api_key (str): API ключ для Stability AI.
    
    Returns:
    tuple: (отрерайченный текст, промпт для изображения, сгенерированное изображение)
    """
    rewritten_text = rewrite_for_kids(text, rewrite_prompt)
    image_prompt = generate_image_prompt(rewritten_text)
    image = generate_image(image_prompt, api_key)
    return rewritten_text, image_prompt, image

def test_full_process():
    """
    Функция для тестирования полного процесса обработки текста и генерации изображения.
    """
    test_text = """Криптовалюты представляют собой цифровые или виртуальные валюты, функционирующие на основе технологии блокчейн, которая обеспечивает их децентрализацию и защиту от подделки. Наиболее известным примером является Bitcoin, созданный в 2009 году анонимным разработчиком или группой разработчиков под псевдонимом Сатоши Накамото."""
    rewrite_prompt = "Ты - учитель, объясняющий сложные финансовые концепции детям 10 лет. Используй простые слова и понятные аналогии."
    api_key = 'sk-m1jiwIw50dffANjG6CCzGpG4gxhZgmvcXAsoAOsh8KOVG75f'
    
    print("Тестирование полного процесса")
    print("Исходный текст:", test_text)
    
    try:
        rewritten_text, image_prompt, image = process_text_and_generate_image(test_text, rewrite_prompt, api_key)
        print("\nОтрерайченный текст:", rewritten_text)
        print("\nПромпт для изображения:", image_prompt)
        image.save("./out/generated_image_from_text.png")
        print("\nИзображение успешно сгенерировано и сохранено как 'generated_image_from_text.png'")
    except Exception as e:
        print(f"Ошибка в процессе: {e}")

if __name__ == "__main__":
    test_full_process()