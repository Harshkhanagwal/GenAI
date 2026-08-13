from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity

with open("data/sample.txt", "r") as file:
    text = file.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", ". ", "\n", " ", ""]
)

chunks = splitter.split_text(text)

# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i + 1} | Length: {len(chunk)}")
#     print(chunk)
#     print("-" * 50)



model = SentenceTransformer("all-MiniLM-L6-v2")

# first_chunk = chunks[0]
# embedding = model.encode(first_chunk)

# print(type(embedding))
# print(len(embedding))
# print(embedding[:10])

# embeddedChunks = []
# for chunk in chunks:
#     embeddedChunks.append(model.encode(chunk))

# # print(embeddedChunks)
# print(embeddedChunks.shape)

question = "What is Retrieval Augmented Generation?"

quesEmbedding = model.encode(question)