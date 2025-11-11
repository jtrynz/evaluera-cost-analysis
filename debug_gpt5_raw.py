#!/usr/bin/env python3
"""
Debug-Script um GPT-5 Response-Struktur zu sehen
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

test_prompt = """Analysiere: ISO 4028-10.9-(ZN-NI)-M10×1,25×45

Gebe ein JSON zurück:
{"norm": "ISO 4028", "diameter_mm": 10, "length_mm": 45, "mass_g": 27.74}"""

print("Sende Request an GPT-5...")
response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "Du bist Ingenieur. Antworte nur als JSON."},
        {"role": "user", "content": test_prompt}
    ],
    max_completion_tokens=500
)

print("\n" + "=" * 80)
print("ROHE RESPONSE-STRUKTUR:")
print("=" * 80)
print(f"Type: {type(response)}")
print(f"Choices: {len(response.choices)}")
print(f"\nChoice[0]:")
print(f"  message type: {type(response.choices[0].message)}")
print(f"  message content: '{response.choices[0].message.content}'")
print(f"  message role: {response.choices[0].message.role}")

# Prüfe ob es ein refusal Feld gibt (GPT-5 Feature)
if hasattr(response.choices[0].message, 'refusal'):
    print(f"  message refusal: {response.choices[0].message.refusal}")

print(f"\nFull message attributes:")
for attr in dir(response.choices[0].message):
    if not attr.startswith('_'):
        try:
            value = getattr(response.choices[0].message, attr)
            if not callable(value):
                print(f"  {attr}: {value}")
        except:
            pass

print("\n" + "=" * 80)
print("CONTENT ANALYSIS:")
print("=" * 80)
content = response.choices[0].message.content
if content:
    print(f"Length: {len(content)}")
    print(f"First 500 chars:\n{content[:500]}")
else:
    print("⚠️ CONTENT IS EMPTY OR NONE!")
