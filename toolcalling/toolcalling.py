import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import json

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
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get the weather for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

msg = input("Ask : ")


message = {
    "role" : role,
    "content" : msg
}

messages = [message]

res = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

print()

tool_call = res.choices[0].message.tool_calls[0]

print("\nTool Call:")
print(tool_call)

arguments = tool_call.function.arguments

arguments = json.loads(arguments)

print("\nArguments:")
print(arguments)


tool_result = get_weather(arguments["city"])

print("\nTool Result:")
print(tool_result)



messages.append(res.choices[0].message)



print("\nTool Call ID:")
print(tool_call.id)



print("\nMessages:")
print(messages)

messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": json.dumps(tool_result)
})

print(messages)


res = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

print(res)

print()
