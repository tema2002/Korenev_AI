import requests
from config import OPENAI_API_KEY

def summarize_text(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = """
    Проанализируйте предоставленный текст и выполните следующие задачи:

    1. Создайте краткое название (не более 10 слов), отражающее основную идею текста.
    2. Напишите краткое саммари текста (не более 3 предложений).
    3. Создайте презентацию из 8-12 слайдов на основе предоставленного текста. Каждый слайд должен содержать ключевые идеи и самую важную информацию. Следуйте этим правилам:

    - Первый слайд должен быть вводным, представляющим тему (используйте созданное название).
    - Последний слайд должен содержать заключение или итоги.
    - Каждый слайд должен иметь чёткий заголовок.
    - Используйте маркированные списки для представления основных пунктов.
    - Включайте только самую важную и релевантную информацию.
    - Если в тексте есть ключевые цифры, статистика или примеры, обязательно включите их.
    - Если уместно, предложите идеи для визуализации (графики, диаграммы, изображения).
    - Сохраняйте последовательность и логическую связь между слайдами.

    Формат вывода:
    НАЗВАНИЕ: [Краткое название текста]
    САММАРИ: [Краткое саммари текста]

    ПРЕЗЕНТАЦИЯ:
    #### 1. [Название текста (из пункта 1)]
    - [Ключевой пункт 1]
    - [Ключевой пункт 2]

    #### 2. [Заголовок слайда]
    - [Ключевой пункт 1]
    - [Ключевой пункт 2]
      [Подпункт 1]
      [Подпункт 2]
    ...

    Преобразуйте следующий текст, точно следуя этому формату:
    """
    
    data = {
        "model": "gpt-4o-2024-08-06",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    content = response.json()['choices'][0]['message']['content']
    
    # Разделяем полученный контент на название, саммари и презентацию
    lines = content.split('\n')
    title = lines[0].replace('НАЗВАНИЕ: ', '').strip()
    summary = lines[1].replace('САММАРИ: ', '').strip()
    presentation = '\n'.join(lines[3:])  # Пропускаем пустую строку после саммари
    
    return title, summary, presentation

# Пример использования:
# title, summary, presentation = summarize_text(your_text_here)