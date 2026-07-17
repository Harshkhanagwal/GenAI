import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()


load_dotenv()
myapi = os.getenv("GROQ_API_KEY")

if not myapi:
    raise ValueError("API key not found")


client=Groq(api_key=myapi)
model = "openai/gpt-oss-120b"


job_description="""
Description
Do you want to solve real customer problems through innovative technology? Do you enjoy working on scalable services in a collaborative team environment? Do you want to see your code directly impact millions of customers worldwide?

At Amazon, we hire the best minds in technology to innovate and build on behalf of our customers. Customer obsession is part of our company DNA, which has made us one of the world's most beloved brands.

Our Software Development Engineers (SDEs) use modern technology to solve complex problems while seeing their work's impact first-hand. The challenges SDEs solve at Amazon are meaningful and influence millions of customers, sellers, and products globally. We seek individuals passionate about creating new products, features, and services while managing ambiguity in an environment where development cycles are measured in weeks, not years.

At Amazon, we believe in ownership at every level. As an SDE-I, you'll own the entire lifecycle of your code - from design through deployment and ongoing operations. This ownership mindset, combined with our commitment to operational excellence, ensures we deliver the highest quality solutions for our customers.

We're looking for curious minds who think big and want to define tomorrow's technology. At Amazon, you'll grow into the high-impact engineer you know you can be, supported by a culture of learning and mentorship. Every day brings exciting new challenges and opportunities for personal growth.
Key job responsibilities
• Collaborate and communicate effectively with experienced cross-disciplinary Amazonians to design, build, and operate innovative products and services that delight our customers, while participating in technical discussions to drive solutions forward.
• Design and develop scalable solutions using cloud-native architectures and microservices in a large distributed computing environment.
• Participate in code reviews and contribute to technical documentation.
• Build and maintain resilient distributed systems that are scalable, fault-tolerant, and cost-effective.
• Leverage and contribute to the development of GenAI and AI-powered tools to enhance development productivity while staying current with emerging technologies.
• Write clean, maintainable code following best practices and design patterns.
• Work in an agile environment practicing CI/CD principles while participating in operational responsibilities including on-call duties.
• Demonstrate operational excellence through monitoring, troubleshooting, and resolving production issues.
Basic Qualifications
- Experience with at least one general-purpose programming language such as Java, Python, C++, C#, Go, Rust, or TypeScript
- Experience with data structure implementation, basic algorithm development, and/or object-oriented design principles
- Currently has, or is in the process of obtaining a bachelor’s degree in Computer Science, Computer Engineering, Data Science, Information Systems, or related STEM fields
- Must be 18 years of age of older
Preferred Qualifications
- Experience from previous technical internship(s) or demonstrated project experience
- Experience with one or more of the following: AI tools for development productivity, Cloud platforms (preferably AWS), Database systems (SQL and NoSQL), Contributing to open-source projects, Version control systems, Debugging and troubleshooting complex systems
- Demonstrated ability to learn and adapt to new technologies quickly
- Basic understanding of software development lifecycle (SDLC)
- Strong problem-solving and analytical skills
- Excellent written and verbal communication skills
"""


# --------------------------------------------------------------------------------------------------------------------------

class JobDescription(BaseModel):
    role:str
    required_skills:list[str]
    preferred_skills:list[str]
    minimum_experience:float | None
    education_reqirements:list[str]
    responsibilities : list[str]


jobDescription_schema = JobDescription.model_json_schema()

system_prompt = f"""

You are a expert HR assistant AI model

your job is to analyze job descriptions and extract structured information from them.

return ONLY valid JSON matching this schema:
{jobDescription_schema}

Note: 
Don't return the schema itself,
don't return fields like "properties", "title" pr "types",
fill the schema with actual information extracted from the job description 

if minimum experience is not mentioned, return null.
if information for a list is missing, return an empty list.

do not invent information.
"""


user_prompt = f"Analyze the following job description and give Json of that, job description : {job_description}"


message_system={
    "role" :"system",
    "content": system_prompt
}

message_user={
    "role":"user",
    "content":user_prompt
}

response_format={
    "type":"json_object"
}

messages=[message_system, message_user]


res = client.chat.completions.create(model=model, messages=messages, response_format=response_format)

raw_jb_json = res.choices[0].message.content

# print(raw_jb_json)

import json
job_data=json.loads(raw_jb_json)
job = JobDescription(**job_data)



# --------------------------------------------------------------------------------------------------------------------------


class MatchResult(BaseModel):
    score : float
    details:dict

class Experience(BaseModel):
    company:str | None = None
    role:str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used : list[str] = []

class Resume(BaseModel):
    name: str | None = None
    email : str | None = None
    phone : str | None = None

    total_experience_years : float | None = None
    skills : list[str] = []
    experiences:list[Experience] = []
    projects:list[str] = []
    certification:list[str] = []


resume_schema= Resume.model_json_schema()

def final_score(job, resume):
    match_schema = MatchResult.model_json_schema()
    prompt = f"""
        You are a HR recruiter 

        compare the candidates resume with the Job description.

        JOB description:
        {job.model_dump_json(indent = 2)}

        candidate_resume:
        {
            resume.model_dump_json(indent=2)
        }

        return json matching this schema:
        {match_schema}

        give me :
        1. candidate name
        2. matching skills
        3. missing important skills
        4. wheather experience requirement is met 
        5. overall match percentage from 0 to 100
        6. a short final verdict

        keep the response concise and easy to read.
    """

    message={
        "role" : "user",
        "content" : prompt
    }

    messages=[message]

    response_format={
        "type":"json_object"
    }

    res = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    data = json.loads(res.choices[0].message.content)

    return MatchResult(**data)

# --------------------------------------------------------------------------------------------------------------------------

def parse_resume(resume_txt):

    system_prompt = f"""
    You are an expert resume parser,

    extract information from the resume based on its meaning, not only based on exact section headings.

    different resumes may use different headings.

    for example:
    - Experience
    - Professional Experience
    - Work History 
    - Employment
    - internships

    these may all contain relevant experience,

    skills may also appear in the skill section, work experience, internships or projects.

    return only valid JSON matching this schema:
    {
        resume_schema
    }

    note : 
    1. do not invent information.
    2. if a value is not available, return null.
    3. if a list has no information, return an empty list.
    4. Include internship inside experiences.
    5. Extract skills mentioned across the entire resume.
    """

    user_prompt = f"""
        parse the follwing resume:
        {resume_txt}
    """

    message_system={
        "role" : "system",
        "content" : system_prompt
    }

    message_user={
        "role":"user",
        "content" : user_prompt
    }

    messages = [message_system, message_user]

    response_format = {
        "type" : "json_object"
    }

    res = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    raw_data = res.choices[0].message.content
    data = json.loads(raw_data)
    resume = Resume(**data)
    return resume

from pypdf import PdfReader

def read_pdf(file_path):
    reader = PdfReader(file_path)

    txt = "" 

    for page in reader.pages:
        page_txt = page.extract_text()

        if page_txt:
            txt += page_txt + " \n"

    return txt

def read_resume(file_path):
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)
    else:
        return None
    
resume_folder = Path("resumes")

all_results=[]

for file_path in resume_folder.iterdir():
    
    if file_path.suffix.lower() not in [".pdf", ".docx"] :
        continue

    print("\n\nProcessing........", file_path.name)

    resume_txt = read_resume(file_path)
    parsed_resume= parse_resume(resume_txt)

    time.sleep(5)
    result = final_score(job, parsed_resume)

    time.sleep(5)

    all_results.append({
        "name" : parsed_resume.name,
        "score" : result.score,
        "details" : result.details
    })

all_results.sort(key=lambda candidate:candidate["score"], reverse=True)


for rslt in all_results:
        print("------------------------------------------------------------------")
        print(rslt["name"] + "\n")
        print(f'{rslt["score"]}%')
        print("\n" + f'{rslt["details"]}' + "\n")
        print("------------------------------------------------------------------")



