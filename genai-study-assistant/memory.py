import json
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage


HISTORY_FIlE = Path("./history.json")

def save_history(history):
    data = []

    for message in history:
        data.append({
            "role": message.type,
            "content" : message.content
        })

    with open(HISTORY_FIlE, "w") as file:
        json.dump(data, file, indent=4)


def load_history():
    if not HISTORY_FIlE.exists():
        return []

    with open(HISTORY_FIlE, "r") as file:
        data = json.load(file)

    history = []

    for message in data:
        if message["role"] == "human":
            history.append(
                HumanMessage(content=message["content"])
            )
        elif message["role"] == "ai":
            history.append(
                AIMessage(content=message["content"])
            )

    return history

