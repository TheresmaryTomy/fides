import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system="You are a Catholic liturgical expert. Return ONLY valid JSON, no other text, no markdown backticks.",
    messages=[{
        "role": "user",
        "content": "Give me Mass readings for: Tuesday of the 11th week of Ordinary Time. Return JSON with keys: first_reading (with reference and summary), psalm (with reference and response), gospel (with reference and summary), saint (string)"
    }]
)

print(response.content[0].text)
