import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

try:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say hello in one line!"}]
    )
    print("✅ Groq API is working!")
    print("Response:", response.choices[0].message.content)

except Exception as e:
    print("❌ Error:", e)