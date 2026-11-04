from langchain_core.tools import tool

@tool
def calculator(a: int, b: int) -> int:
    """Multiply two integers and return the result."""
    return a * b