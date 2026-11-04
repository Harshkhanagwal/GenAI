
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

from memory import save_history, load_history

load_dotenv()


class DevProfiie(BaseModel):
    skills: list[str]
    experience: int | None = None
    role: str | None = None


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI study assistant."),
    ("placeholder", "{history}"),
    ("human", "{question}"),
])


def main():
    model = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.7,
    )

    print("--------------------------------")
    print("GenAI Study Assistant - Ask me anything about programming.")
    print("--------------------------------")
    print("Type 'exit' to quit.")
    print("--------------------------------")

    # Load previously saved conversation
    history = load_history()

    print(f"Loaded {len(history)} previous messages.")

    chain = prompt | model

    while True:
        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            print("Assistant: ", end="", flush=True)

            full_response = ""

            for chunk in chain.stream({
                "history": history,
                "question": question
            }):
                content = chunk.content

                if isinstance(content, str):
                    print(content, end="", flush=True)
                    full_response += content

            print()

            # Update conversation history
            history.append(HumanMessage(content=question))
            history.append(AIMessage(content=full_response))

            # Persist updated conversation
            save_history(history)

        except Exception as error:
            print(f"\nRequest failed: {error}")


if __name__ == "__main__":
    main()
