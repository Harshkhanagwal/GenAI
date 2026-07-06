import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_groq_api = os.getenv("GROQ_API_KEY")

if not my_groq_api:
    raise ValueError("API key not found")

client = Groq(api_key=my_groq_api)

model="llama-3.3-70b-versatile"
role="user"
prompt="hello, how are you"

message = {
    "role" : role,
    "content" : prompt
}

messages = [message]

res = client.chat.completions.create(model=model, messages=messages)
print()

print(res )
print()
print("-----------------------------------------")
print()
print(res.choices[0].message.content)

print()
