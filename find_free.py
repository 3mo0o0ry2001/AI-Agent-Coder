import requests
import json

response = requests.get("https://openrouter.ai/api/v1/models")
models = json.loads(response.text)['data']

print("🆓 Available Free Models on OpenRouter right now:")
for m in models:
    if "free" in m['id']:
        print(f" - {m['id']}")