import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from time import sleep


load_dotenv()
myapi = os.getenv("GROQ_API_KEY")

if not myapi:
    raise ValueError("API key not found")


#LLM setup 
client = Groq(api_key=myapi)
model="llama-3.3-70b-versatile"


jd = """We are looking for a Full Stack Developer with experience in React.js, Node.js, and MongoDB. The candidate should be able to build responsive web applications, develop REST APIs, and work with databases. Basic knowledge of Git and problem-solving skills are required.
    Required Skills

- Proficiency in HTML5, CSS3, and JavaScript (ES6+)
- Experience with React.js
- Strong knowledge of Node.js and Express.js
- Experience with MongoDB or SQL databases
- Understanding of RESTful APIs
- Familiarity with Git and GitHub
- Basic knowledge of authentication (JWT/OAuth)
- Understanding of responsive web design
- Ability to debug and troubleshoot web applications
- Good problem-solving and communication skills
"""
resume = """
John Doe
Email: john.doe@email.com
Phone: +1 234 567 8901

Summary
Motivated Full Stack Developer with experience in building web applications using React.js, Node.js, and MongoDB.

Skills
- React.js
- Node.js
- Express.js
- MongoDB
- HTML, CSS, JavaScript
- Git

Experience
Full Stack Developer Intern
ABC Technologies
Jan 2025 - Jun 2025
- Developed responsive web pages using React.
- Built REST APIs with Node.js and Express.
- Integrated MongoDB for data storage.

Education
Bachelor of Computer Science
XYZ University
2021 - 2025
"""


def call_llm(system_prompt, user_prompt) :
    sys_msg = {
        "role" : "system",
        "content" : system_prompt
    }
    user_msg ={
        "role" : "user",
        "content" : user_prompt
    }
    messages = [sys_msg, user_msg]

    res = client.chat.completions.create(model=model, messages=messages)

    return res.choices[0].message.content


def s1_res_extract() :
    #extract skills from resume

    global resume

    system_prompt = """
        you are a professional HR assistant, extract the skills of user from the given job description. only return the skills no other data and do not invent any data which is not present
    """

    user_prompt = f"extract skills from this Job description {resume}"

    return call_llm(system_prompt, user_prompt)

def s2_jd_extract() :
    #extract skills from JD

    global resume

    system_prompt = """
        you are a professional HR assistant, extract the skills of user from the given job description. only return the skills no other data and do not invent any data which is not present
    """

    user_prompt = f"extract skills from this JD {resume}"

    return call_llm(system_prompt, user_prompt)

def s3_match(candidate, jd_skills) :

    #match the skills of user with JD

    sys_prompt = """
        you are a professional HR assistant, compare the skills of  candidate and the skills present in JD produce a final matching score between 1 and 100, also prodoce a short verdice whther the candidate is good fit or not and why.
    """

    user_prompt = f"skills from this JD {jd_skills} and skills from the resume {candidate}"

    return call_llm(sys_prompt, user_prompt)


candidate = s1_res_extract()

sleep(2)
jd_skills = s2_jd_extract()
sleep(2)

final = s3_match(candidate, jd_skills)
sleep(2)


print(final)