text = """
Python is a popular programming language.
It is widely used in AI and machine learning.
Python has libraries like NumPy and Pandas.
It was created by Guido van Rossum.
"""

chunk_size = 50
overlap = 10

start = 0

while start < len(text):

    # Ideal ending position
    target_end = min(start + chunk_size, len(text))

    # If we've reached the end, take everything remaining
    if target_end == len(text):
        chunk = text[start:target_end]
        print("Chunk:")
        print(chunk)
        break

    # Find the nearest space before target_end
    cut_position = text.rfind(" ", start, target_end)

    # No space found → use target_end
    if cut_position == -1:
        cut_position = target_end

    # Create chunk
    chunk = text[start:cut_position]

    print("Chunk:")
    print(chunk)
    print("--------------------")

    # Calculate next starting position
    new_start = cut_position - overlap

    # Safety: start MUST move forward
    if new_start <= start:
        new_start = cut_position

    start = new_start