import asyncio
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7
)

async def main():
    async for chunk in model.astream("Explain Python in two sentences."):
        if chunk.content:
            print(chunk.content, end="", flush=True)

    print()

asyncio.run(main())