from langchain_text_splitters import RecursiveCharacterTextSplitter

with open("data/sample.txt", "r") as file:
    text = file.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", ". ", "\n", " ", ""]
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1} | Length: {len(chunk)}")
    print(chunk)
    print("-" * 50)