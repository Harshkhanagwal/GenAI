import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import json

# importing our actual tool/function
from tools.weather import get_weather
from tools.todos import create_todo
from tools.todos import get_todo

# load stuff from .env
load_dotenv()

# grab Groq API key
my_groq_api = os.getenv("GROQ_API_KEY")

# just making sure the key actually exists
if not my_groq_api:
    raise ValueError("API key not found")


# create Groq client
client = Groq(api_key=my_groq_api)

model = "llama-3.3-70b-versatile"
role = "user"



available_tools = {
    "get_weather": get_weather,
    "create_todo": create_todo,
    "get_todo": get_todo
}



# --------------------------------------------------
# TOOL DEFINITION
# --------------------------------------------------
# Here we're basically telling the LLM:
# "yo, you have this tool available if you need it"
#
# IMPORTANT:
# this does NOT actually run get_weather()
# it only tells the AI:
# - tool name
# - what it does
# - what arguments it needs


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",

            # helps the AI understand when this tool should be used
            "description": "Get the current weather for a city",

            # basically the input format/schema for our function
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get the weather for"
                    }
                },

                # city must be provided
                "required": ["city"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "create_todo",
        "description": "Create a todo item for the user and store it in the list",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Category of the todo, for example shopping or learning"
                },
                "task": {
                    "type": "string",
                    "description": "The actual todo task the user wants to store"
                }
            },
            "required": ["task", "category"]
        }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_todo",
            "description" : "return all avilable todos of user"
        }
    }
]

system_prompt = """
You are a friendly and conversational AI assistant with a slightly sarcastic sense of humor.

Response rules:
- Respond naturally, like a human conversation.
- Keep responses concise by default, preferably 1-2 sentences.
- Do not give long explanations unless the user explicitly asks for details.
- Use light sarcasm occasionally when appropriate, but never be rude or insulting.
- Answer the user's question directly without unnecessary information.
- If the user asks for a detailed explanation, provide more detail as needed.
"""


message_system={
    "role" :"system",
    "content": system_prompt
}

messages = [message_system]


while True:
    msg = input("USER : ")

    if msg == "end":
        break

    message = {
        "role": role,
        "content": msg
    }
    messages.append(message)

    res = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = res.choices[0].message
    tool_calls = getattr(assistant_message, "tool_calls", None)

    if tool_calls:
        print("AI : Tool call received")
        # We're grabbing the first requested tool here.
        tool_call = res.choices[0].message.tool_calls[0]

        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        

        print("Tool:", tool_name)
        arguments = arguments or {}
        print("Arguments:", arguments)


        selected_function = available_tools.get(tool_name)

        if selected_function:
            tool_result = selected_function(**arguments)
        else:
            tool_result = "Tool not found"

        # if tool_name == "get_weather":
        #     tool_result = get_weather(arguments["city"])
        # elif tool_name == "create_todo":
        #     tool_result = create_todo(arguments["category"], arguments["task"])
        # elif tool_name == "get_todo":
        #     tool_result = get_todo()
        # else:
        #     tool_result = "tool not found"
        
        messages.append(res.choices[0].message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })

        res = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        final_message = res.choices[0].message

        print("AI: " + final_message.content)
        messages.append(final_message)

    else:
        # print("Normal response")
        print("AI :" + assistant_message.content)
        messages.append(assistant_message)





# --------------------------------------------------
# USER MESSAGE
# --------------------------------------------------

# msg = input("Ask : ")

# message = {
#     "role": role,
#     "content": msg
# }

# messages = [message]


# # --------------------------------------------------
# # FIRST LLM CALL
# # --------------------------------------------------
# # We send:
# # 1. user's message
# # 2. available tools
# #
# # tool_choice="auto" means:
# # LLM decides whether it needs a tool or not

# res = client.chat.completions.create(
#     model=model,
#     messages=messages,
#     tools=tools,
#     tool_choice="auto"
# )

# print()


# # --------------------------------------------------
# # GET THE TOOL CALL
# # --------------------------------------------------
# # If the AI decides:
# # "I need weather data"
# #
# # it returns a tool_call instead of actually calling
# # the Python function itself.
# #
# # We're grabbing the first requested tool here.

# tool_call = res.choices[0].message.tool_calls[0]

# print("\nTool Call:")
# print(tool_call)


# # --------------------------------------------------
# # GET ARGUMENTS GENERATED BY AI
# # --------------------------------------------------
# # arguments usually comes back as a JSON STRING
# #
# # something like:
# # '{"city":"Bhopal"}'

# arguments = tool_call.function.arguments


# # convert JSON string -> Python dictionary
# #
# # '{"city":"Bhopal"}'
# # becomes
# # {"city": "Bhopal"}

# arguments = json.loads(arguments)

# print("\nArguments:")
# print(arguments)


# # --------------------------------------------------
# # ACTUALLY RUN THE TOOL
# # --------------------------------------------------
# # THIS is where our Python function actually runs.
# #
# # Important idea:
# # LLM asked us to call the tool.
# # Our Python code is the one actually calling it.

# tool_result = get_weather(arguments["city"])

# print("\nTool Result:")
# print(tool_result)


# # --------------------------------------------------
# # SAVE AI'S TOOL REQUEST IN MESSAGE HISTORY
# # --------------------------------------------------
# # We need this because the next LLM call needs to know:
# # "oh yeah, I requested this tool earlier"

# messages.append(res.choices[0].message)


# print("\nTool Call ID:")
# print(tool_call.id)


# print("\nMessages:")
# print(messages)


# messages.append({
#     "role": "tool",
#     "tool_call_id": tool_call.id,
#     "content": json.dumps(tool_result)
# })

# print(messages)


# # --------------------------------------------------
# # SECOND LLM CALL
# # --------------------------------------------------
# # Now the AI has:
# #
# # user question
# #      ↓
# # its own tool request
# #      ↓
# # actual tool result
# #
# # So now it can use that data to generate
# # a normal human-readable answer.

# res = client.chat.completions.create(
#     model=model,
#     messages=messages,
#     tools=tools,
#     tool_choice="auto"
# )


# # --------------------------------------------------
# # FINAL ANSWER
# # --------------------------------------------------

# print("\nFinal Answer:")
# print(res.choices[0].message.content)

# print()