#%%
import openai
import config

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

def test_rewrite():
    """
    Функция для тестирования работы rewrite_for_kids.
    """
    test_text = """Криптовалюты представляют собой цифровые или виртуальные валюты, функционирующие на основе технологии блокчейн, которая обеспечивает их децентрализацию и защиту от подделки. Наиболее известным примером является Bitcoin, созданный в 2009 году анонимным разработчиком или группой разработчиков под псевдонимом Сатоши Накамото."""
    
    print("Тест 1: Стандартный промпт")
    print("Оригинальный текст:")
    print(test_text)
    print("\nПереписанный текст:")
    print(rewrite_for_kids(test_text, "Ты - учитель, объясняющий сложные финансовые концепции детям 10 лет. Используй простые слова и понятные аналогии."))
    
    print("\nТест 2: Пользовательский промпт")
    custom_prompt = "Ты - бизнес-аналитик, объясняющий финансовые концепции профессионалам. Используй деловой стиль и соответствующую терминологию."
    print("Оригинальный текст:")
    print(test_text)
    print("\nПереписанный текст с пользовательским промптом:")
    print(rewrite_for_kids(test_text, custom_prompt))

if __name__ == "__main__":
    test_rewrite()
#%%