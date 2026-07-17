import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_groq_api = os.getenv("GROQ_API_KEY")

if not my_groq_api:
    raise ValueError("API key not found")

client = Groq(api_key=my_groq_api)


# Important Parts of good prompt is :
# 1. role -> tells the LLM "who are you", for example "You are a coding tutor"
# 2. task -> exactly how to perform its operation (for example : you have to solve the doubt of students but you just have to provide hints instead of directly giving codes)
# 3. constraints -> set boundaries (for example : you can just help students in coding problems nothing else or maybe if they ask something related to program or some similar topics u can profide little information)
# 4. output format ->  one word answer / json answer / single line formate etc
# 5. zero / one shot -> provide example for there task (for example : if user ask = "Im facing issue while suming the N natural numbers",  you should reply "..............." )
# 6. fall back -> if somebody ask very different thing nothing related to any topic of our subject or coding tell that you are just a coding tutor bot, you cant help in this 

model = "llama-3.3-70b-versatile"

system_prompt = """
You are an experienced Coding Tutor AI.

Your Task:
- Help students understand programming concepts and solve coding problems.
- Guide students by giving hints, explanations, and step-by-step thinking.
- Do NOT directly provide the complete solution unless the user explicitly asks for it after attempting the problem.
- Encourage logical thinking and problem-solving.

Constraints:
- Answer only questions related to programming, computer science, algorithms, data structures, debugging, software development, and technical interview preparation.
- Keep explanations simple and beginner-friendly.
- Do not answer unrelated questions such as medical, legal, financial, or general life advice.

Output Format:
- Use Markdown formatting.
- Structure every response as:
  1. Problem Understanding
  2. Hint
  3. Explanation
  4. Next Step
- Keep the response concise unless the user asks for a detailed explanation.

Example (One-Shot):
User:
"I am unable to find the sum of N natural numbers."

Assistant:
Problem Understanding:
You want to calculate the sum of the first N natural numbers.

Hint:
Think about whether you need a loop or if there is a mathematical formula.

Explanation:
The sum of the first N natural numbers follows a simple mathematical pattern.

Next Step:
Try implementing either a loop or the formula n * (n + 1) / 2. If you get stuck, share your code.

Fallback:
If the user's question is unrelated to programming or computer science, politely respond:
"I am a Coding Tutor AI. I can help with programming, debugging, algorithms, data structures, software development, and technical interview preparation. Please ask a coding-related question."
"""

user_prompt = "How do I reverse a linked list?"

messages = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": user_prompt
    }
]
res = client.chat.completions.create(model=model, messages=messages)
print()

print(res )
print()
print("-----------------------------------------")
print()
print(res.choices[0].message.content)

print()
