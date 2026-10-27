from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel,ValidationError

load_dotenv()



class DevProfiie(BaseModel) :
    skills : list[str]
    experience : int | None
    role : str | None


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI study assistant."),
    ("human", "{question}"),
])


def main():
    model = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.7,
    )

    # structured_model = model.with_structured_output(DevProfiie,  method="json_schema")

    # chain = prompt | structured_model

  
    # try:
    #     response = chain.invoke({
    #         "question": (
    #             "role is full stack genAI developer and works on React, Redux, Tailwind, Python, FastAPI, MongoDB. i have 3+ years of expirece "
    #             "Do not invent data that is not mentioned."
    #         )
    #     })
    #     print(response.skills)
    #     print(response.experience)
    #     print(response.role)          
    # except ValidationError as err:
    #     print("invalid data")
    #     print(err)




    print("--------------------------------")
    print("GenAI Study Assistant - Ask me anything about programming.")
    print("--------------------------------")
    print("Type 'exit' to quit.")
    print("--------------------------------")

    history = []

    chain = prompt | model


    while True:
        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        if not question:
            continue


        try:
            # messages = prompt.format_messages(
            #     history=history,
            #     question=question,
            # )

            print("Assistant : ")

            full_response =""

            try:
                for chunk in chain.stream({
                            "history": history,
                            "question": question
                     }):
                    print(chunk.content, end="", flush=True)
                    full_response += chunk.content
                        # print(f"\nAssistant: {response.content}\n")
            
                history.append(HumanMessage(content=question))
                history.append(AIMessage(content=full_response))
            
            except Exception as err:
                print("Something went wrong while calling the AI.")
                print("Error:", err)
           
            print()

        except Exception as error:
            print(f"Request failed: {error}")


if __name__ == "__main__":
    main()