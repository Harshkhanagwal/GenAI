import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel


load_dotenv()
my_g_api = os.getenv("GROQ_API_KEY")

if not my_g_api:
    raise ValueError("API KEY NOT FOUND")

client = Groq(api_key=my_g_api)
model="llama-3.3-70b-versatile"


class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema = Ticket.model_json_schema()

response_format={
    "type" : "json_object"
}

system_prompt=f"""
    you are a LLM in IT department of a company your work is get details of the raised tickets, Extrack the name, email and issue of user strictly based on this schema. {schema} and give data in JSON.
"""

message_system={
    "role" : "system",
    "content" : system_prompt
}

role="user"
txt="hello my name is Jack. i'm from delhi, my email is harsh@mail.com, Im not able to connect with my PROD jump server"
prompt =f"""
this is the raised ticket {txt}
"""

message= {
    "role" : role,
    "content" : prompt
}


messages=[message_system, message]


res = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

print()
# print(res)
print("-----------------------------------------")


import json
raw_json = res.choices[0].message.content
data_file = json.loads(raw_json)
ticket =Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.issue)

print()
