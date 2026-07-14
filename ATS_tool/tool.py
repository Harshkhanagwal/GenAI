import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader

load_dotenv()
myapi = os.getenv("GROQ_API_KEY")

if not myapi:
    raise ValueError("API key not found")

reader = PdfReader("Resume.pdf")


resume_data = ""

for page in reader.pages:
    resume_data += page.extract_text() + "\n"


jd = ""

with open("JD.txt", "r", encoding="utf-8") as f:
    jd = f.read()


client = Groq(api_key=myapi)
model="llama-3.3-70b-versatile"


class report(BaseModel):
    name:str
    skills:list
    score:int
    description:str


schema = report.model_json_schema()

response_format={
    "type":"json_object"
}

system_prompt=f"""
    You are an ATS tool which reads the data of resume and compare it with given data of job description and as per that generate and report with name of applicant from resume and its skills in list format or you can say array, with score as how much percentage its matching with Job description also a descripition where you'll mention way we should select or why we should not, as per the {schema} give response in JSON.
"""

message_system={
    "role":"system",
    "content" : system_prompt
}

role="user"
prompt=f"""this is the resume data : {resume_data} and n this is job description : {jd} """

message={
    'role' : role,
    'content': prompt
}

messages=[message_system, message]

res = client.chat.completions.create(model=model, messages=messages, response_format=response_format)


print()

print("----------------------------------------------------------------------")

print(res.choices[0].message.content)

print("----------------------------------------------------------------------")

print()

