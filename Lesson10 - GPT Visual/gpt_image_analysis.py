#%%
import base64
import requests
from config import OPENAI_API_KEY, PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_input, is_url=True):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    if is_url:
        image_payload = {
            "type": "image_url",
            "image_url": {
                "url": image_input
            }
        }
    else:
        base64_image = encode_image(image_input)
        image_payload = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image? Ответь на русском"
                    },
                    image_payload
                ]
            }
        ],
        "max_tokens": 300
    }

    proxies = {
        "http": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}",
        "https": f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", 
                             headers=headers, 
                             json=payload, 
                             proxies=proxies)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Пример использования
if __name__ == "__main__":
    # Анализ изображения по URL
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    result = analyze_image(image_url)
    print("Анализ изображения по URL:")
    print(result)

    # Анализ локального изображения
    # local_image_path = "path/to/your/local/image.jpg"
    # result = analyze_image(local_image_path, is_url=False)
    # print("\nАнализ локального изображения:")
    # print(result)

# %%
