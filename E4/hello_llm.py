import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_groq_api = os.getenv("GROQ_API_KEY")

if not my_groq_api:
    raise ValueError("API KEY NOT FOUND")

client = Groq(api_key=my_groq_api)

model="llama-3.3-70b-versatile"
role="user"
prompt1="hello"
prompt2="how are you"
prompt3="what can you do for me as a AI modal"

prompts=[prompt1, prompt2, prompt3]

for prompt in prompts:
    message = {
        "role" : role,
        "content" : prompt
    }

    messages =[message]

    res = client.chat.completions.create(model=model, messages=messages)
    usage=res.usage
    print("-----------------------------------------")
    print(f"Prompt: {prompt}  \n--> prompt token : {usage.prompt_tokens} \n--> completion token : {usage.completion_tokens} \n--> total token : {usage.prompt_tokens + usage.prompt_tokens}")
    print("-----------------------------------------")

    print(res )
    print()
    print("-----------------------------------------")
    print()
    print( "res \n", res.choices[0].message.content)
    print("-----------------------------------------")
    print()