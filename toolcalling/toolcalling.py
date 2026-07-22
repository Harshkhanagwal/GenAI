import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

#tools import
from tools.weather import get_weather

load_dotenv()
my_groq_api = os.getenv("GROQ_API_KEY")

if not my_groq_api:
    raise ValueError("API key not found")

client = Groq(api_key=my_groq_api)

model="llama-3.3-70b-versatile"
role="user"


tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_weather",
            "description" :"get the current weather for a city"
        }
    }
]

msg = input("Ask : ")


message = {
    "role" : role,
    "content" : msg
}

messages = [message]


res = client.chat.completions.create(model=model, messages=messages, tools=tools)


print()

print(res.choices[0].message.content)

print()
