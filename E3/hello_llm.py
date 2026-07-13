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
prompt="hello, we are thinking to launch new product in you food chain which is chicken burger suggest name for perticualr burger we have used sweet and chilly souce combo in it. just give one names."

message_system={
    "role" : "system",
    "content" : "You are my branding manager and marketing manager too, you help me to get audiance attention"
}

message = {
    "role" : role,
    "content" : prompt
}

messages = [message_system, message]
# temperature by default is 0 
res = client.chat.completions.create(model=model, messages=messages)
print()

# print(res )
print()
print("-----------------------------------------")
print()
print(res.choices[0].message.content)

print()
