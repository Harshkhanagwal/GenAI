from memory import save_history, load_history
from langchain_core.messages import HumanMessage, AIMessage

# Create sample conversation
history = [
    HumanMessage(content="What is Python?"),
    AIMessage(content="Python is a programming language.")
]

# Save conversation
save_history(history)

# Restore conversation
loaded_history = load_history()

# Display restored messages
for message in loaded_history:
    print(message.type, ":", message.content)
    